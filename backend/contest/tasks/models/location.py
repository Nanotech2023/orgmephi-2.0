import enum

from common import get_current_db
from common.util import db_get_or_raise
from user.models import City, Country

db = get_current_db()


class LocationEnum(enum.Enum):
    OlympiadLocation = "OlympiadLocation"
    OnlineOlympiadLocation = "OnlineOlympiadLocation"
    RussiaOlympiadLocation = "RussiaOlympiadLocation"
    OtherOlympiadLocation = "OtherOlympiadLocation"


class OlympiadLocation(db.Model):
    """
    This class describing olympiad contest location

    location_id: id of location
    location: where olympiad take place // link to online service

    """

    __tablename__ = 'olympiad_location'

    location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    location_type = db.Column(db.Enum(LocationEnum))

    __mapper_args__ = {
        'polymorphic_identity': LocationEnum.OlympiadLocation,
        'with_polymorphic': '*',
        "polymorphic_on": location_type
    }


def add_online_location(db_session, url):
    """
    Create new location
    """
    location = OnlineOlympiadLocation(
        url=url,
    )
    db_session.add(location)
    return location


class OnlineOlympiadLocation(OlympiadLocation):
    url = db.Column(db.String)

    __tablename__ = 'olympiad_location_online'

    __mapper_args__ = {
        'polymorphic_identity': LocationEnum.OnlineOlympiadLocation,
        'with_polymorphic': '*'
    }


def add_russia_location(db_session, city_name, region_name, address):
    """
    Create new location
    """

    db_get_or_raise(City, "name", city_name)
    db_get_or_raise(City, "region_name", region_name)

    location = RussiaOlympiadLocation(
        city_name=city_name,
        region_name=region_name,
        address=address,
    )
    db_session.add(location)
    return location


class RussiaOlympiadLocation(OlympiadLocation):
    city_name = db.Column(db.String)
    region_name = db.Column(db.String)
    address = db.Column(db.String)

    city = db.relationship('City')

    __tablename__ = 'olympiad_location_russia'

    __mapper_args__ = {
        'polymorphic_identity': LocationEnum.RussiaOlympiadLocation,
        'with_polymorphic': '*'
    }


db.ForeignKeyConstraint((RussiaOlympiadLocation.city_name, RussiaOlympiadLocation.region_name),
                        (City.name, City.region_name))


def add_other_location(db_session, country_name, location):
    """
    Create new location
    """
    db_get_or_raise(Country, "name", country_name)

    location = OtherOlympiadLocation(
        country_name=country_name,
        location=location,
    )
    db_session.add(location)
    return location


class OtherOlympiadLocation(OlympiadLocation):
    country_name = db.Column(db.String, db.ForeignKey(Country.name))
    location = db.Column(db.String)

    country = db.relationship('Country')

    __tablename__ = 'olympiad_location_other'

    __mapper_args__ = {
        'polymorphic_identity': LocationEnum.OtherOlympiadLocation,
        'with_polymorphic': '*'
    }
