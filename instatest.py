import datetime
import getpass
import json
import logging
import os
import random
import string
from os.path import expanduser
import configparser
from multiprocessing import Lock

import boto3
import dateutil.parser
from boto3 import Session

from moto import mock_sts

_mock_sts = mock_sts()
_mock_sts.start()

class EnvironmentMock():

    roles = ['dev', 'test', 'admin']

    def __init__(self, name=None, region=None):
        # Defaults to name=instatruck and region=Australia unless specified
        self._role = EnvironmentMock.get_roles()[0]
        self._name = name or 'instatruck'

        # public property
        self.region = region or "Australia"

    @staticmethod
    def get_account_number():
        return '13579'

    def get_name(self):
        return self._name

    @staticmethod
    def get_roles():
        return EnvironmentMock.roles

    def get_role(self):
        return self._role

    def set_role(self, role):
        self._role = role


class Wrapper(object):
    _role_session_cache = {}
    _session_cache = {}
    _console_available = True
    _locks = {'all': Lock()}

    @staticmethod
    def get_session(environment, duration_seconds=86400):

        with Wrapper._locks['all']:

            if environment.get_account_number() not in Wrapper._locks:
                Wrapper._locks[environment.get_account_number()] = Lock()
                Wrapper._locks[environment.get_account_number() + '-role-session-lock'] = Lock()

        # TODO: whilst we've solve concurrency problems there's an opporuntity here to improve performance through reuse
        with Wrapper._locks[environment.get_account_number()]:

            session = Wrapper._get_cached_role_session(environment)

            if session:
                return session

        with Wrapper._locks['all']:

            session = Wrapper._get_user_session_from_disk_cache(environment)

            if environment.get_role():

                if session is None:
                    session = Wrapper._get_user_session(environment, duration_seconds)

                with Wrapper._locks[environment.get_account_number() + '-role-session-lock']:

                    if not Wrapper._get_user_role(environment):
                        return Wrapper._set_user_role(environment, session)

                    session = Wrapper._get_session_for_assumed_role(environment, session)

            else:

                session = Session(region_name=environment.region, profile_name=os.environ.get('Wrapper_PROFILE', 'default'))

        return session

    @staticmethod
    def _get_mfa_serial():
        try:
            if os.environ.get('Wrapper_PROFILE'):
                mfa_serial = Wrapper.get_mfa_serial(aws_profile=os.environ.get('Wrapper_PROFILE'))
            else:
                mfa_serial = Wrapper.get_mfa_serial()
        except:
            mfa_serial = None
        return mfa_serial

    @staticmethod
    def _get_user_session(environment, duration_seconds):
        log = logging.getLogger(__name__)

        if not Wrapper._console_available:
            raise Exception('Not authenticated to Wrapper. Run authenticate command.')

        # find a MFA Serial
        log.debug('creating user session for ' + environment.get_name())

        mfa_serial = Wrapper._get_mfa_serial()

        if mfa_serial is None:
            log.debug('Couldn\'t find MFA serial, getting session without MFA')
            # get a session token
            response = Session().client('sts').get_session_token(DurationSeconds=duration_seconds)
        else:
            # prompt for mfa serial
            token = getpass.getpass('Enter MFA Token: ')

            # get a session token
            response = Session().client('sts').get_session_token(
                DurationSeconds=duration_seconds,
                SerialNumber=mfa_serial,
                TokenCode=token
            )
        data = response['Credentials']
        data['Expiration'] = str(data['Expiration'])  # to help serialization
        Wrapper._save_session_to_disk_cache(data)

        session = Wrapper._get_user_session_from_disk_cache(environment)

        return session

    @staticmethod
    def _get_session_for_assumed_role(environment, session, role=None):

        log = logging.getLogger(__name__)

        if role is None:
            role = Wrapper._get_user_role(environment) or environment.get_role()

        log.info('Assuming role ' + 'arn:aws:iam::' + environment.get_account_number() + ':role/' + role.strip())
        response = session.client('sts').assume_role(
            RoleArn='arn:aws:iam::' + environment.get_account_number() + ':role/' + role.strip(),
            RoleSessionName=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        )

        data = response['Credentials']

        log = logging.getLogger(__name__)
        log.debug('creating role session for ' + environment.get_name())

        session = boto3.Session(
            aws_access_key_id=data['AccessKeyId'],
            aws_secret_access_key=data['SecretAccessKey'],
            aws_session_token=data['SessionToken'],
            region_name=environment.region
        )

        Wrapper._role_session_cache[environment.get_account_number()] = (session, data)

        return session

    @staticmethod
    def _get_cached_role_session(environment):

        log = logging.getLogger(__name__)

        if environment.get_role():

            session_key = environment.get_account_number()

            if session_key in Wrapper._role_session_cache:
                session, data = Wrapper._role_session_cache[session_key]
                expiration = data['Expiration']
                if expiration > datetime.datetime.now(expiration.tzinfo):
                    log.debug('used cached role session for ' + environment.get_name())
                    return session

        return None

    @staticmethod
    def _get_user_session_from_disk_cache(environment):

        file_name = Wrapper._get_cached_token_file_name()
        if not os.path.exists(file_name):
            return None

        try:
            with open(file_name, 'r') as token_file:
                data = json.loads(token_file.read())
        except:
            return None

        expiration = dateutil.parser.parse(data['Expiration'])
        if expiration <= datetime.datetime.now(expiration.tzinfo):
            return None

        session = boto3.Session(
            aws_access_key_id=data['AccessKeyId'],
            aws_secret_access_key=data['SecretAccessKey'],
            aws_session_token=data['SessionToken'],
            region_name=environment.region
        )

        return session

    @staticmethod
    def _save_session_to_disk_cache(session):

        log = logging.getLogger(__name__)

        data = session
        file_name = Wrapper._get_cached_token_file_name()
        log.debug('saving session to disk. file name = ' + file_name)
        with open(file_name, 'w') as token_file:
            token_file.write(json.dumps(data))

        log.debug('saved session to disk')

    @staticmethod
    def _get_cached_token_file_name():
        profile = os.environ.get("Wrapper_PROFILE") or 'default';
        file_name = 'cached-session-token-' + profile + '.json'
        directory = expanduser('~/insterview/cache')

        if not os.path.exists(directory):
            os.makedirs(directory)

        return directory + '/' + file_name

    @staticmethod
    def get_mfa_serial(aws_profile=None, aws_config_file='~/.aws/config'):

        log = logging.getLogger(__name__)
        log.debug('retrieving mfa serial')

        # use specified section for serial - for contractors who will have more than onw mfa serial
        if os.environ.get('Wrapper_PROFILE'):
            aws_profile = os.environ.get('Wrapper_PROFILE')

        if aws_profile:
            section = 'profile ' + aws_profile
            config = configparser.RawConfigParser()
            config.read(expanduser(aws_config_file))
            if not config.has_section(section):
                raise 'Requested profile ' + aws_profile + ' does not exist in ' + aws_config_file

            return config.get(section, 'mfa_serial')

        # otherwise just find one
        else:

            with open(expanduser(aws_config_file), 'r') as content_file:
                for line in content_file.readlines():
                    if 'mfa_serial' in line:
                        return line.split('=')[1].strip()

            raise Exception('Attempting to generate config based on existing config failed...'
                            ' need at least one MFA serial configured in your ~/.aws/config file')

    @staticmethod
    def _set_user_role(environment, session):
        log = logging.getLogger(__name__)
        for role in environment.get_roles():
            try:
                log.debug('trying role: ' + role)
                result = Wrapper._get_session_for_assumed_role(environment, session, role)
                Wrapper._save_user_role(environment, role)
                environment.set_role(role)
                log.debug('setting role: ' + role)
                return result
            except:
                continue

        log.debug('Did not find any roles you can use for environment ' + environment.get_name())
        return session

    @staticmethod
    def _save_user_role(environment, role):
        file_name = os.path.expanduser('~/insterview/' + environment.get_account_number() + '.role')
        with open(file_name, 'w') as role_file:
            return role_file.write(role)

    @staticmethod
    def _get_user_role(environment):
        file_name = os.path.expanduser('~/insterview/' + environment.get_account_number() + '.role')
        if not os.path.exists(file_name):
            return None

        with open(file_name, 'r') as role_file:
            return role_file.read()

    @classmethod
    def set_console_available(cls):
        Wrapper._console_available = True


# Tests
if __name__=="__main__":
    env1 = EnvironmentMock()

    s1 = Wrapper.get_session(env1)
    s2 = Wrapper.get_session(env1)
    print(s1, s2)
    assert s1.get_credentials().token == s2.get_credentials().token

    # More tests

