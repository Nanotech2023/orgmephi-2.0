from . import *

DEFAULT_INDEX = 0
ERROR_ID = 1500


@pytest.fixture
def client(client_visitor):
    client_visitor.set_prefix('contest/tasks/unauthorized')
    yield client_visitor
