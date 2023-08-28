from wrapper import Wrapper

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



# Tests
if __name__=="__main__":
    env1 = EnvironmentMock()

    s1 = Wrapper.get_session(env1)
    s2 = Wrapper.get_session(env1)
    print(s1, s2)
    assert s1.get_credentials().token == s2.get_credentials().token

    # More tests

