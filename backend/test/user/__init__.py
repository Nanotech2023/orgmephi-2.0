from .. import *


test_user_info = {
    "document": {
        "code": "123-456",
        "document_type": "RFPassport",
        "issue_date": "2021-09-02",
        "issuer": "string",
        "number": "123456",
        "series": "4520"
    },
    "dwelling": {
        "city": "test",
        "country": "native",
        "region": "test",
        "rural": True
    },
    "gender": "Male",
    "limitations": {
        "hearing": True,
        "movement": True,
        "sight": True
    },
    "phone": "+78005553535",
    "place_of_birth": "string"
}


test_university_info = {
    "citizenship": "native",
    "city": "test",
    "grade": 1,
    "region": "test",
    "university": {
        "country": "native",
        "university": "test"
    }
}


test_school_info = {
    "grade": 1,
    "location": {
        "city": "test",
        "country": "native",
        "region": "test",
        "rural": True
    },
    "name": "string",
    "number": 0,
    "school_type": "School"
}


@pytest.fixture
def test_group():
    from user.models import Group
    grp = Group(name='Test')
    test_app.db.session.add(grp)
    test_app.db.session.commit()
    yield grp


@pytest.fixture
def test_country_native():
    from user.models import Country
    country = Country(name=test_app.config['ORGMEPHI_NATIVE_COUNTRY'])
    test_app.db.session.add(country)
    test_app.db.session.commit()
    yield country


@pytest.fixture
def test_country_foreign():
    from user.models import Country
    country = Country(name='not' + test_app.config['ORGMEPHI_NATIVE_COUNTRY'])
    test_app.db.session.add(country)
    test_app.db.session.commit()
    yield country


@pytest.fixture
def test_region():
    from user.models import Region
    region = Region(name='test')
    test_app.db.session.add(region)
    test_app.db.session.commit()
    yield region


@pytest.fixture
def test_city(test_region):
    from user.models import City
    city = City(name='test')
    city.region = test_region
    test_app.db.session.add(city)
    test_app.db.session.commit()
    yield city


@pytest.fixture
def test_university(test_country_native):
    from user.models import University
    university = University(name='test')
    university.country = test_country_native
    test_app.db.session.add(university)
    test_app.db.session.commit()
    yield university
