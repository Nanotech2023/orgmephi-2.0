from . import *


def step_init_client(client, state):
    reset_db(test_app)
    state.client = OrgMephiTestingClient(test_app.app.test_client())


def step_init_admin(client, state):
    from user.models import init_user, UserTypeEnum, UserRoleEnum
    import datetime

    password_hash = test_app.password_policy.hash_password('test-password', False)
    user = init_user('admin', password_hash, UserRoleEnum.admin, UserTypeEnum.internal)
    user.password_changed = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
    test_app.db.session.add(user)
    test_app.db.session.commit()
    state.admin = dict()
    state.admin['id'] = user.id
    state.admin['username'] = user.username
    state.admin['password'] = 'test-password'


steps_init = [step_init_client, step_init_admin]