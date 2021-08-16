from common import get_current_db, get_current_app
from .auth import User
from .reference import City, Country

db = get_current_db()
app = get_current_app()


class UserInfo(db.Model):
    """
        Personal user info ORM class

        Attributes:

        id: id of the info
        email: email address of the user
        first_name: user's first name
        middle_name: user's middle name
        second_name: user's second name
        date_of_birth: user's date of birth
    """

    __table_name__ = 'user_info'

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    email = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    second_name = db.Column(db.String)
    date_of_birth = db.Column(db.Date)

    user = db.relationship('User', back_populates='user_info', lazy='select')
    dwelling = db.relationship('Dwelling', back_populates='user_info', lazy='select', uselist=False,
                               cascade='save-update, merge, delete, delete-orphan')


class Dwelling(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(UserInfo.user_id), primary_key=True)
    russian = db.Column(db.Boolean)
    rural = db.Column(db.Boolean)

    user_info = db.relationship('UserInfo', back_populates='dwelling', lazy='select')

    __mapper_args__ = {
        'polymorphic_identity': None,
        'with_polymorphic': '*',
        "polymorphic_on": russian
    }


class DwellingRussia(Dwelling):
    city_name = db.Column(db.String, db.ForeignKey(City.name))
    city = db.relationship('City')

    __mapper_args__ = {
        'polymorphic_identity': True,
        'with_polymorphic': '*'
    }


class DwellingOther(Dwelling):
    country_name = db.Column(db.String, db.ForeignKey(Country.name))
    location = db.Column(db.String)
    country = db.relationship('Country')

    __mapper_args__ = {
        'polymorphic_identity': False,
        'with_polymorphic': '*'
    }
