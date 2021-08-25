from common import get_current_db, get_current_app
from .reference import City, Country
from user.util import get_unfilled

db = get_current_db()
app = get_current_app()


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    russian = db.Column(db.Boolean, nullable=False)
    rural = db.Column(db.Boolean)

    __mapper_args__ = {
        'polymorphic_identity': None,
        'with_polymorphic': '*',
        "polymorphic_on": russian
    }

    _required_fields = ['russian', 'rural']

    def unfilled(self):
        return get_unfilled(self, self._required_fields, [])


class LocationRussia(Location):
    city_name = db.Column(db.String)
    region_name = db.Column(db.String)
    city = db.relationship('City')

    __mapper_args__ = {
        'polymorphic_identity': True,
        'with_polymorphic': '*'
    }

    _required_fields = ['city_name', 'region_name']

    def unfilled(self):
        return get_unfilled(self, self._required_fields, []) + super().unfilled()


db.ForeignKeyConstraint((LocationRussia.city_name, LocationRussia.region_name), (City.name, City.region_name))


class LocationOther(Location):
    country_name = db.Column(db.String, db.ForeignKey(Country.name))
    location = db.Column(db.String)
    country = db.relationship('Country')

    __mapper_args__ = {
        'polymorphic_identity': False,
        'with_polymorphic': '*'
    }

    _required_fields = ['country_name', 'location']

    def unfilled(self):
        return get_unfilled(self, self._required_fields, []) + super().unfilled()
