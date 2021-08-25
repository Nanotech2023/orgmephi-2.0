from common import get_current_db, get_current_app

db = get_current_db()
app = get_current_app()


class Country(db.Model):
    """
        Known countries ORM class

        Attributes:

        id: id of the country
        name: name of the country
    """
    __table_name__ = 'country'

    name = db.Column(db.String, nullable=False, unique=True, primary_key=True)


@app.db_prepare_action()
def populate_country():
    """
     pre-populate known country table with predefined values
    """
    from common.util import db_populate
    names = open(db.get_app().config['ORGMEPHI_COUNTRY_FILE'], encoding='utf8').read().splitlines()
    db_populate(db.session, Country, [Country(name=name) for name in names], 'name')
    db.session.commit()


class Region(db.Model):
    """
        Known RF regions ORM class

        Attributes:

        id: id of the region
        name: name of the region
    """

    name = db.Column(db.String, nullable=False, unique=True, primary_key=True)
    cities = db.relationship('City', back_populates='region', lazy='dynamic')


@app.db_prepare_action()
def populate_regions():
    """
     pre-populate known region table with predefined values
    """
    from common.util import db_populate
    names = open(db.get_app().config['ORGMEPHI_REGION_FILE'], encoding='utf8').read().splitlines()
    db_populate(db.session, Region, [Region(name=name) for name in names], 'name')
    db.session.commit()


class City(db.Model):
    """
        Known RF cities ORM class

        Attributes:

        id: id of the city
        name: name of the city
        region_name: name of city's region
    """

    region_name = db.Column(db.String, db.ForeignKey(Region.name), primary_key=True)
    name = db.Column(db.String, nullable=False, primary_key=True)
    region = db.relationship('Region', back_populates='cities')


def _read_city(name, region_name):
    from common.util import db_get_one_or_none
    city = City(name=name)
    region = db_get_one_or_none(Region, 'name', region_name)
    if region is not None:
        city.region_name = region.name
        return city
    else:
        app.app.logger.warning('City "%s" depends on region "%s" which is not known', name, region_name)


@app.db_prepare_action()
def populate_cities():
    """
     pre-populate known city table with predefined values
    """
    from common.util import db_populate
    lines: list[str] = open(db.get_app().config['ORGMEPHI_CITY_FILE'], encoding='utf8').read().splitlines()
    values = [line.split(sep=',') for line in lines]
    cities = [_read_city(value[0].strip(), value[1].strip()) for value in values if len(value) >= 2]
    cities = [city for city in cities if city is not None]

    db_populate(db.session, City, cities, keys=['name', 'region_name'])
    db.session.commit()


class University(db.Model):
    """
        Known universities ORM class

        Attributes:

        id: id of the university
        name: name of the university
        country_name" name of university's country
    """
    __table_name__ = 'university'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    country_name = db.Column(db.String, db.ForeignKey(Country.name))
    country = db.relationship('Country')


def _read_university(name, country_name):
    from common.util import db_get_one_or_none
    uni = University(name=name)
    if country_name is not None:
        country = db_get_one_or_none(Country, 'name', country_name)
        if country is not None:
            uni.country_name = country.name
        else:
            app.app.logger.warning('University "%s" depends on country "%s" which is not known', name, country_name)
    return uni


@app.db_prepare_action()
def populate_university():
    """
    pre-populate known university table with predefined values
    """
    from common.util import db_populate
    lines: list[str] = open(db.get_app().config['ORGMEPHI_UNIVERSITY_FILE'], encoding='utf8').read().splitlines()
    values = [line.split(sep=',') for line in lines]
    unis = [_read_university(value[0].strip(), value[1].strip() if len(value) >= 2 else None) for value in values
            if len(value) > 0]

    db_populate(db.session, University, unis, 'name')
    db.session.commit()
