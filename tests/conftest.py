from functools import partial

import pytest
from django.core.management import call_command

from helpers import UserRepositoryMock


@pytest.fixture()
def repository():
    return UserRepositoryMock()


@pytest.fixture()
def load_data():
    return partial(call_command, 'loaddata')
