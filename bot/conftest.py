def pytest_make_parametrize_id(config, val):  # noqa: W0613
    return repr(val)
