import os

import pytest

ENV_VARS = {
    "VJUDGE_BASE_URL": "https://vjudge.net",
    "VJUDGE_USERNAME": "vjudge",
    "VJUDGE_PASSWORD": "password",
}


@pytest.fixture(scope="session", autouse=True)
def tests_setup_and_teardown():
    # Will be executed before the first test
    old_environ = dict(os.environ)
    os.environ.update(ENV_VARS)

    yield
    # Will be executed after the last test
    os.environ.clear()
    os.environ.update(old_environ)
