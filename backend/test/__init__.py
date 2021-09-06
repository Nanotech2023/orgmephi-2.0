import pytest

from common.testing import get_test_app, OrgMephiTestingClient, reset_db

from aggregate import module
print(__package__)
# noinspection DuplicatedCode
test_app = get_test_app(module)


@pytest.fixture
def client_visitor():
    reset_db(test_app)
    with test_app.app.test_client() as client:
        yield OrgMephiTestingClient(client)


@pytest.fixture
def client_admin(client_visitor):
    client_visitor.fake_login(username='admin', role='Admin', user_id=1)
    yield client_visitor


@pytest.fixture
def client_creator(client_visitor):
    client_visitor.fake_login(username='creator', role='Creator', user_id=2)
    yield client_visitor


@pytest.fixture
def client_school(client_visitor):
    client_visitor.fake_login(username='school', role='Participant', user_id=3)
    yield client_visitor


@pytest.fixture
def client_university(client_visitor):
    client_visitor.fake_login(username='university', role='Participant', user_id=4)
    yield client_visitor
