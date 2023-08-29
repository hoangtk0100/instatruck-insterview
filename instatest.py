from wrapper import Wrapper, dateparser, datetime, exists
from unittest.mock import patch, MagicMock, mock_open
from datetime import timedelta
from constant import *
from os import remove
import unittest
import json

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


class TestWrapper(unittest.TestCase):
    # Initialize mock data
    _env = MagicMock(EnvironmentMock())

    _config_file = '~/.aws/config'
    _role = 'dev'
    _not_existing_profile_name = 'not_existing_profile'
    _profile_name = 'dummy_profile'
    _mfa_serial = 'dummy_mfa_serial'
    _input_token = 'dummy_input_token'
    _get_aws_mfa_serial_exception = 'Attempting to generate config based on existing config failed... need at least one MFA serial configured in your %s file' % _config_file

    _datetime_format = '%Y-%m-%dT%H:%M:%SZ'
    _duration_seconds = 3600
    _any_expiration = dateparser.parse('2023-08-28T12:00:00Z')
    _expiration = datetime.now(_any_expiration.tzinfo) + timedelta(seconds=_duration_seconds)
    _credentials = {
        ACCESS_KEY_ID_KEY: 'dummy_access_key_id',
        SECRET_ACCESS_KEY_KEY: 'dummy_secret_access_key',
        SESSION_TOKEN_KEY: 'dummy_session_token',
        EXPIRATION_KEY: _expiration
    }

    def tearDown(self):
        # Remove cached files after each test
        cache_file = Wrapper._get_cached_token_file_name()
        if exists(cache_file):
            remove(cache_file)

    def test_get_cached_role_session_without_role(self):
      mock_env = self._env
      mock_env.get_role.return_value = None

      session = Wrapper._get_cached_role_session(mock_env)
      self.assertIsNone(session)

    @patch('wrapper.Wrapper._role_session_cache', {'1234': (MagicMock(), {EXPIRATION_KEY: _expiration})})
    def test_get_cached_role_session_with_role_no_session_key(self):
        mock_env = self._env
        mock_env.get_role.return_value = self._role
        mock_env.get_account_number.return_value = '5678'

        session = Wrapper._get_cached_role_session(mock_env)
        self.assertIsNone(session)

    @patch('wrapper.Wrapper._role_session_cache', {'1234': (MagicMock(), {EXPIRATION_KEY: _expiration - timedelta(seconds=_duration_seconds)})})
    def test_get_cached_role_session_with_role_expired_session(self):
        mock_env = self._env
        mock_env.get_role.return_value = self._role
        mock_env.get_account_number.return_value = '1234'

        session = Wrapper._get_cached_role_session(mock_env)
        self.assertIsNone(session)

    @patch('os.path.exists', return_value=False)
    def test_get_user_session_from_disk_cache_file_not_found(self, mock_exists):
        session = Wrapper._get_user_session_from_disk_cache(self._env)
        self.assertIsNone(session)
    
    @patch('builtins.open', side_effect=Exception)
    def test_get_user_session_from_disk_cache_error_read_file(self, mock_open):
        session = Wrapper._get_user_session_from_disk_cache(self._env)
        self.assertIsNone(session)

    @patch('builtins.open', mock_open(read_data=json.dumps({EXPIRATION_KEY: (_expiration - timedelta(seconds=_duration_seconds)).strftime(_datetime_format)})))
    def test_get_user_session_from_disk_cache_expired_session(self):
        session = Wrapper._get_user_session_from_disk_cache(self._env)
        self.assertIsNone(session)
    
    @patch('configparser.RawConfigParser')
    @patch('wrapper.Wrapper._get_wrapper_profile', return_value=_profile_name)
    def test_get_mfa_serial_with_configparser_existed_profile(self, mock_get_wrapper_profile, mock_rawconfigparser):
        mock_config = mock_rawconfigparser.return_value
        mock_config.has_section.return_value = True
        mock_config.get.return_value = self._mfa_serial

        mfa_serial = Wrapper._get_mfa_serial()
        self.assertEqual(mfa_serial, self._mfa_serial)

        profile = mock_get_wrapper_profile.return_value
        section = f'profile {profile}'
        mock_config.has_section.assert_called_once_with(section)
        mock_config.get.assert_called_once_with(section, 'mfa_serial')

    @patch('configparser.RawConfigParser')
    @patch('wrapper.Wrapper._get_wrapper_profile', return_value=_not_existing_profile_name)
    def test_get_mfa_serial_with_configparser_not_existing_profile(self, mock_get_wrapper_profile, mock_rawconfigparser):
        mock_rawconfigparser.return_value.has_section.return_value = False

        with self.assertRaises(Exception) as ctx:
            Wrapper._get_aws_mfa_serial()
        
        profile = mock_get_wrapper_profile.return_value
        self.assertEqual(str(ctx.exception), f'Requested profile {profile} does not exist in {self._config_file}')

    @patch('wrapper.Wrapper._get_wrapper_profile', return_value=None)
    @patch('builtins.open', mock_open(read_data=f'mfa_serial = {_mfa_serial}'))
    def test_get_mfa_serial_without_profile_existed_mfa_serial(self, mock_get_wrapper_profile):
        self.assertIsNone(mock_get_wrapper_profile.return_value)
        mfa_serial = Wrapper._get_mfa_serial()
        self.assertEqual(mfa_serial, self._mfa_serial)

    @patch('wrapper.Wrapper._get_wrapper_profile', return_value=None)
    @patch('builtins.open', side_effect=Exception(_get_aws_mfa_serial_exception))
    def test_get_mfa_serial_without_profile_file_not_found(self, mock_open, mock_get_wrapper_profile):
        self.assertIsNone(mock_get_wrapper_profile.return_value)
        with self.assertRaises(Exception) as ctx:
            Wrapper._get_aws_mfa_serial()

        mock_open.assert_called_once()
        self.assertEqual(ctx.exception, mock_open.side_effect)

    @patch('wrapper.Wrapper._get_wrapper_profile', return_value=None)
    @patch('builtins.open', mock_open(read_data='other_config = any_value'))
    def test_get_mfa_serial_without_profile_not_existing_mfa_serial(self, mock_get_wrapper_profile):
        self.assertIsNone(mock_get_wrapper_profile.return_value)
        with self.assertRaises(Exception) as ctx:
            Wrapper._get_aws_mfa_serial()
        self.assertEqual(str(ctx.exception), self._get_aws_mfa_serial_exception)

    @patch.object(Wrapper, '_console_available', False)
    def test_get_user_session_without_mfa_serial_console_unavailable(self):
        with self.assertRaises(Exception) as ctx:
            Wrapper._get_user_session(self._env, duration_seconds=self._duration_seconds)
        self.assertEqual(str(ctx.exception), 'Not authenticated to Wrapper. Run authenticate command.')
    
    @patch.object(Wrapper, '_console_available', True)
    @patch('wrapper.Wrapper._get_mfa_serial', return_value=None)
    @patch('wrapper.Wrapper._save_session_to_disk_cache')
    def test_get_user_session_without_mfa_serial(self, mock_save_session_to_disk_cache, mock_get_mfa_serial):
        session = Wrapper._get_user_session(self._env, duration_seconds=self._duration_seconds)
        self.assertIsNotNone(session)
        mock_get_mfa_serial.assert_called_once()
        mock_save_session_to_disk_cache.assert_called_once()

    def test_get_session(self):
        session1 = Wrapper.get_session(self._env)
        self.assertIsNotNone(session1)

        session2 = Wrapper.get_session(self._env)
        self.assertIsNotNone(session2)

        credentials1 = session1.get_credentials()
        credentials2 = session2.get_credentials()
        self.assertEqual(credentials1.access_key, credentials2.access_key)
        self.assertEqual(credentials1.secret_key, credentials2.secret_key)
        self.assertEqual(credentials1.token, credentials2.token)

    def test_get_session_different_duration(self):
        session1 = Wrapper.get_session(self._env, 3000)
        self.assertIsNotNone(session1, 3600)

        session2 = Wrapper.get_session(self._env)
        self.assertIsNotNone(session2)

        credentials1 = session1.get_credentials()
        credentials2 = session2.get_credentials()
        self.assertEqual(credentials1.access_key, credentials2.access_key)
        self.assertEqual(credentials1.secret_key, credentials2.secret_key)
        self.assertEqual(credentials1.token, credentials2.token)


if __name__ == '__main__':
    unittest.main()
