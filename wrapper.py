from datetime import datetime
from getpass import getpass
import json
import logging
import os
import random
import string
from os.path import expanduser, exists
import configparser
from multiprocessing import Lock
from constant import *

import boto3
import dateutil.parser as dateparser
from boto3 import Session

from moto import mock_sts

_mock_sts = mock_sts()
_mock_sts.start()

CACHE_PATH = '~/insterview/cache'
BASE_PROFILE_PATH = '~/insterview'
DEFAULT = 'default'
DEFAULT_SESSION_DURATION = 86400

class Wrapper(object):
    _role_session_cache = {}
    _session_cache = {}
    _console_available = True
    _locks = {'all': Lock()}
    _log = logging.getLogger(__name__)

    @staticmethod
    def get_session(environment, duration_seconds=DEFAULT_SESSION_DURATION):
        key = environment.get_account_number()

        with Wrapper._locks['all']:
            if key not in Wrapper._locks:
                Wrapper._locks[key] = Lock()
                Wrapper._locks[f'{key}-role-session-lock'] = Lock()

        with Wrapper._locks[key]:
            # Check if the session was cached by another thread
            if key in Wrapper._session_cache:
                return Wrapper._session_cache[key]
        
            session = Wrapper._get_cached_role_session(environment)
            if session:
                return session

        with Wrapper._locks['all']:
            session = Wrapper._get_user_session_from_disk_cache(environment)

            if environment.get_role():
                if session is None:
                    session = Wrapper._get_user_session(environment, duration_seconds)

                with Wrapper._locks[f'{key}-role-session-lock']:
                    if not Wrapper._get_user_role(environment):
                        return Wrapper._set_user_role(environment, session)

                    session = Wrapper._get_session_for_assumed_role(environment, session)

            else:
                session = Session(
                    region_name=environment.region,
                    profile_name=Wrapper._get_wrapper_profile(DEFAULT)
                )

        return session

    @staticmethod
    def _get_mfa_serial():
        try:
            return Wrapper._get_aws_mfa_serial()
        except:
            return None

    @staticmethod
    def _get_user_session(environment, duration_seconds):
        if not Wrapper._console_available:
            raise Exception('Not authenticated to Wrapper. Run authenticate command.')

        # find a MFA Serial
        Wrapper._log.debug(f'creating user session for {environment.get_name()}')

        mfa_serial = Wrapper._get_mfa_serial()
        if mfa_serial is None:
            Wrapper._log.debug("Couldn't find MFA serial, getting session without MFA")
            # get a session token
            response = Session().client('sts').get_session_token(DurationSeconds=duration_seconds)
        else:
            # prompt for mfa serial
            token = getpass('Enter MFA Token: ')

            # get a session token
            response = Session().client('sts').get_session_token(
                DurationSeconds=duration_seconds,
                SerialNumber=mfa_serial,
                TokenCode=token
            )

        data = response[CREDENTIALS_KEY]
        data[EXPIRATION_KEY] = str(data[EXPIRATION_KEY])  # to help serialization

        Wrapper._save_session_to_disk_cache(data)

        return Wrapper._get_user_session_from_disk_cache(environment)

    @staticmethod
    def _get_session_for_assumed_role(environment, session, role=None):
        if role is None:
            role = Wrapper._get_user_role(environment) or environment.get_role()

        key = environment.get_account_number()
        role_arn = f'arn:aws:iam::{key}:role/{role.strip()}'

        Wrapper._log.info(f'Assuming role {role_arn}')

        response = session.client('sts').assume_role(
            RoleArn=role_arn,
            RoleSessionName=Wrapper._random_session_name()
        )

        data = response[CREDENTIALS_KEY]

        Wrapper._log.debug(f'creating role session for {environment.get_name()}')

        session = Wrapper._get_aws_session(environment, data)

        Wrapper._role_session_cache[key] = (session, data)

        return session

    @staticmethod
    def _get_cached_role_session(environment):
        if environment.get_role():
            session_key = environment.get_account_number()

            if session_key in Wrapper._role_session_cache:
                session, data = Wrapper._role_session_cache[session_key]
                expiration = data[EXPIRATION_KEY]
                if expiration > datetime.now(expiration.tzinfo):
                    Wrapper._log.debug(f'used cached role session for {environment.get_name()}')
                    return session

        return None

    @staticmethod
    def _get_user_session_from_disk_cache(environment):
        file_name = Wrapper._get_cached_token_file_name()
        if not exists(file_name):
            return None

        try:
            with open(file_name, 'r') as token_file:
                data = json.loads(token_file.read())
        except:
            return None

        expiration = dateparser.parse(data[EXPIRATION_KEY])
        if expiration <= datetime.now(expiration.tzinfo):
            return None

        return Wrapper._get_aws_session(environment, data)

    @staticmethod
    def _save_session_to_disk_cache(session):
        file_name = Wrapper._get_cached_token_file_name()
        Wrapper._log.debug(f'saving session to disk. file name = {file_name}')
        
        with open(file_name, 'w') as token_file:
            token_file.write(json.dumps(session))

        Wrapper._log.debug('saved session to disk')

    @staticmethod
    def _get_cached_token_file_name():
        profile = Wrapper._get_wrapper_profile() or DEFAULT
        file_name = f'cached-session-token-{profile}.json'
        directory = expanduser(CACHE_PATH)

        if not exists(directory):
            os.makedirs(directory)

        return f'{directory}/{file_name}'

    @staticmethod
    def _get_aws_mfa_serial(profile=None, config_file='~/.aws/config'):
        Wrapper._log.debug('retrieving mfa serial')

        # use specified section for serial - for contractors who will have more than one mfa serial
        profile = profile or Wrapper._get_wrapper_profile()

        if profile:
            section = f'profile {profile}'
            config = configparser.RawConfigParser()
            config.read(expanduser(config_file))

            if not config.has_section(section):
                raise Exception(f'Requested profile {profile} does not exist in {config_file}')

            return config.get(section, 'mfa_serial')

        # otherwise just find one
        else:
            with open(expanduser(config_file), 'r') as content_file:
                for line in content_file.readlines():
                    if 'mfa_serial' in line:
                        return line.split('=')[1].strip()

            raise Exception('Attempting to generate config based on existing config failed...'
                            ' need at least one MFA serial configured in your %s file' % config_file)

    @staticmethod
    def _set_user_role(environment, session):
        for role in environment.get_roles():
            try:
                Wrapper._log.debug(f'trying role: {role}')

                result = Wrapper._get_session_for_assumed_role(environment, session, role)
                Wrapper._save_user_role(environment, role)
                environment.set_role(role)

                Wrapper._log.debug(f'setting role: {role}')
                return result
            except:
                continue

        Wrapper._log.debug(f'Did not find any roles you can use for environment {environment.get_name()}')
        return session

    @staticmethod
    def _save_user_role(environment, role):
        file_name = expanduser(f'{BASE_PROFILE_PATH}/{environment.get_account_number()}.role')
        with open(file_name, 'w') as role_file:
            return role_file.write(role)

    @staticmethod
    def _get_user_role(environment):
        file_name = expanduser(f'{BASE_PROFILE_PATH}/{environment.get_account_number()}.role')
        if not exists(file_name):
            return None

        with open(file_name, 'r') as role_file:
            return role_file.read()

    @classmethod
    def enable_console(cls):
        Wrapper._console_available = True
    
    @classmethod
    def disable_console(cls):
        Wrapper._console_available = False

    @staticmethod
    def _get_wrapper_profile(default=None):
        return os.environ.get(WRAPPER_PROFILE_KEY, default)

    @staticmethod
    def _random_session_name(length=8):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    @staticmethod
    def _get_aws_session(environment, data):
        return boto3.Session(
            aws_access_key_id=data[ACCESS_KEY_ID_KEY],
            aws_secret_access_key=data[SECRET_ACCESS_KEY_KEY],
            aws_session_token=data[SESSION_TOKEN_KEY],
            region_name=environment.region
        )