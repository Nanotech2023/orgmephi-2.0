import enum
from common import get_current_db, get_current_app
from .auth import User
from .location import Location
from user.util import get_unfilled

db = get_current_db()
app = get_current_app()


class GenderEnum(enum.Enum):
    """
        Gender enumeration class.
    """

    male = 'Male'
    female = 'Female'


class UserInfo(db.Model):
    """
        Personal user info ORM class

        Attributes:

        id: id of the info
        email: email address of the user
        phone: user's phone number
        first_name: user's first name
        middle_name: user's middle name
        second_name: user's second name
        date_of_birth: user's date of birth
    """

    __table_name__ = 'user_info'

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey(Location.id))
    email = db.Column(db.String, unique=True)
    phone = db.Column(db.String)
    first_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    second_name = db.Column(db.String)
    date_of_birth = db.Column(db.Date)
    place_of_birth = db.Column(db.String)
    gender = db.Column(db.Enum(GenderEnum))
    photo = db.Column(db.LargeBinary)

    user = db.relationship('User', back_populates='user_info', lazy='select')
    dwelling = db.relationship('Location', lazy='select', uselist=False, single_parent=True,
                               cascade='save-update, merge, delete, delete-orphan')
    document = db.relationship('Document', lazy='select', uselist=False,
                               cascade='save-update, merge, delete, delete-orphan')
    limitations = db.relationship('UserLimitations', lazy='select', uselist=False,
                                  cascade='save-update, merge, delete, delete-orphan')

    _required_fields = ['email', 'phone', 'first_name', 'middle_name', 'second_name', 'date_of_birth',
                        'place_of_birth', 'gender', 'dwelling', 'document', 'limitations']

    def unfilled(self):
        return get_unfilled(self, self._required_fields, ['dwelling', 'document', 'limitations'])


class UserLimitations(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(UserInfo.user_id), primary_key=True)
    hearing = db.Column(db.Boolean, nullable=False, default=False)
    sight = db.Column(db.Boolean, nullable=False, default=False)
    movement = db.Column(db.Boolean, nullable=False, default=False)

    _required_fields = ['hearing', 'sight', 'movement']

    def unfilled(self):
        return get_unfilled(self, self._required_fields, [])
