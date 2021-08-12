from common import get_current_db, get_current_app
from .auth import User

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

