import pytest

from common.testing import get_test_app, OrgMephiTestingClient, reset_db

from aggregate import module
print(__package__)
# noinspection DuplicatedCode
test_app = get_test_app(module)


def _generate_user():
    from user.models import init_user, UserTypeEnum, UserRoleEnum
    import datetime
    password_hash = test_app.password_policy.hash_password('test-password', False)
    user = init_user('test', password_hash, UserRoleEnum.unconfirmed, UserTypeEnum.internal)
    user.password_changed = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
    test_app.db.session.add(user)
    test_app.db.session.commit()
    return user


@pytest.fixture
def test_user():
    yield _generate_user()


@pytest.fixture
def test_user_admin():
    from user.models import UserTypeEnum, UserRoleEnum
    user = _generate_user()
    user.username = 'admin'
    user.role = UserRoleEnum.admin
    user.type = UserTypeEnum.internal
    test_app.db.session.commit()
    yield user


@pytest.fixture
def test_user_creator():
    from user.models import UserTypeEnum, UserRoleEnum
    user = _generate_user()
    user.username = 'creator'
    user.role = UserRoleEnum.creator
    user.type = UserTypeEnum.internal
    test_app.db.session.commit()
    yield user


@pytest.fixture
def test_user_school():
    from user.models import UserTypeEnum, UserRoleEnum
    user = _generate_user()
    user.username = 'school'
    user.role = UserRoleEnum.participant
    user.type = UserTypeEnum.school
    test_app.db.session.commit()
    yield user


@pytest.fixture
def test_user_university():
    from user.models import UserTypeEnum, UserRoleEnum
    user = _generate_user()
    user.username = 'university'
    user.role = UserRoleEnum.participant
    user.type = UserTypeEnum.university
    test_app.db.session.commit()
    yield user


@pytest.fixture
def test_users(test_user_admin, test_user_creator, test_user_school, test_user_university):
    yield [test_user_admin, test_user_creator, test_user_school, test_user_university]


@pytest.fixture
def client_visitor():
    reset_db(test_app)
    with test_app.app.test_client() as client:
        yield OrgMephiTestingClient(client)


def _generate_client(client, user):
    client.fake_login(username=user.username, role=user.role.value, user_id=user.id)
    return client


@pytest.fixture
def client_admin(client_visitor, test_user_admin):
    yield _generate_client(client_visitor, test_user_admin)


@pytest.fixture
def client_creator(client_visitor, test_user_creator):
    yield _generate_client(client_visitor, test_user_creator)


@pytest.fixture
def client_school(client_visitor, test_user_school):
    yield _generate_client(client_visitor, test_user_school)


@pytest.fixture
def client_university(client_visitor, test_user_university):
    yield _generate_client(client_visitor, test_user_university)
