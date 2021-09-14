from . import *

DEFAULT_INDEX = 0
ERROR_ID = 1500


@pytest.fixture
def client(client_university):
    client_university.set_prefix('contest/tasks/participant')
    yield client_university

