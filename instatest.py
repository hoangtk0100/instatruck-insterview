from wrapper import Wrapper, EnvironmentMock

# Tests
if __name__=="__main__":
    env1 = EnvironmentMock()

    s1 = Wrapper.get_session(env1)
    s2 = Wrapper.get_session(env1)
    print(s1, s2)
    assert s1.get_credentials().token == s2.get_credentials().token

    # More tests

