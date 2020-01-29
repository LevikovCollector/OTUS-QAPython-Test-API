import pytest


@pytest.fixture
def dog_host():
    return 'https://dog.ceo/api/'


@pytest.fixture
def openbrewerydb_host():
    return 'https://api.openbrewerydb.org/'


@pytest.fixture
def jsonplaceholder_host():
    return 'https://jsonplaceholder.typicode.com/'


def pytest_addoption(parser):
    parser.addoption('--url', action='store', default='https://ya.ru')
    parser.addoption('--status_code', action='store', default='200')


@pytest.fixture
def param_from_user(request):
    return (request.config.getoption('--url'), request.config.getoption('--status_code'))
