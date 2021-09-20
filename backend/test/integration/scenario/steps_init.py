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


def step_init_locations(client, state):
    from user.models import Country, Region, City, University
    country_native = Country(name=test_app.config['ORGMEPHI_NATIVE_COUNTRY'])
    country_foreign = Country(name='not' + test_app.config['ORGMEPHI_NATIVE_COUNTRY'])
    region = Region(name='test')
    city = City(name='test')
    city.region = region
    university = University(name='test')
    university.country = country_native

    test_app.db.session.add(country_native)
    test_app.db.session.add(country_foreign)
    test_app.db.session.add(region)
    test_app.db.session.add(city)
    test_app.db.session.add(university)

    test_app.db.session.commit()

    state.country_native = dict()
    state.country_native['name'] = country_native.name

    state.country_foreign = dict()
    state.country_foreign['name'] = country_foreign.name

    state.region = dict()
    state.region['name'] = region.name

    state.city = dict()
    state.city['name'] = city.name
    state.city['region'] = city.region_name

    state.university = dict()
    state.university['name'] = university.name
    state.university['country'] = university.country_name


def step_init_target_classes(client, state):
    from contest.tasks.models import TargetClass
    classes = [str(target_class) for target_class in range(8, 12)] + ['student']
    target_classes = [TargetClass(target_class=target_class) for target_class in classes]
    for target_class in target_classes:
        test_app.db.session.add(target_class)
    test_app.db.session.commit()

    state.target_classes = [target_class.target_class_id for target_class in target_classes]


steps_init = [step_init_client, step_init_admin, step_init_locations, step_init_target_classes]
