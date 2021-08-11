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

    def serialize(self):
        return \
            {
                'email': self.email,
                'first_name': self.first_name,
                'second_name': self.second_name,
                'middle_name': self.middle_name,
                'date_of_birth': self.date_of_birth.isoformat()
            }

    def update(self, email=None, first_name=None, second_name=None, middle_name=None, date_of_birth=None):
        if email is not None:
            self.email = email
        if first_name is not None:
            self.first_name = first_name
        if second_name is not None:
            self.second_name = second_name
        if middle_name is not None:
            self.middle_name = middle_name
        if date_of_birth is not None:
            self.date_of_birth = date_of_birth


def create_personal_info(email, first_name, second_name, middle_name, date_of_birth):
    user_info = UserInfo(
        email=email,
        first_name=first_name,
        second_name=second_name,
        middle_name=middle_name,
        date_of_birth=date_of_birth
    )
    return user_info
