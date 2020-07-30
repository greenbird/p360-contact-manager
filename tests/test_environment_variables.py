import os

from p360_contact_manager.constants import Argument
from p360_contact_manager.environment_variables import (
    ParseEnvironmentVariables,
)


def test_parsing():
    os.environ[Argument.authkey.as_env()] = 'test'
    parsed = ParseEnvironmentVariables()()
    assert parsed.unwrap()[Argument.authkey.name] == 'test'
