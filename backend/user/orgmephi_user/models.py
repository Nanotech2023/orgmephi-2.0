from orgmephi_user import db
from datetime import datetime
import enum


class UserRoleEnum(enum.Enum):
    user = 1
    creator = 2
    admin = 3
    system = 4


class UserTypeEnum(enum.Enum):
    pre_university = 1
    enrollee = 2
    school = 3
    university = 4
    internal = 5
    pre_register = 6


def _populate_table(table, values):
    for value in values:
        q = db.session.query(table).filter(table.name == value)
        if not db.session.query(q.exists()).scalar():
            instance = table(name=value)
            db.session.add(instance)
    db.session.commit()


class User(db.Model):
    __table_name__ = 'user'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.Enum(UserRoleEnum), nullable=False)
    type = db.Column(db.Enum(UserTypeEnum), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student_info.id'))


class UserInfo(db.Model):
    __table_name__ = 'user_info'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    second_name = db.Column(db.String)
    dateofbirth = db.Column(db.Date)


class StudentInfo(db.Model):
    __table_name__ = 'student_info'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    phone = db.Column(db.String)
    university = db.Column(db.Integer, db.ForeignKey('university.id'))
    custom_university = db.Column(db.String)
    admission_year = db.Column(db.Date)
    university_country = db.Column(db.Integer, db.ForeignKey('country.id'))
    citizenship = db.Column(db.Integer, db.ForeignKey('country.id'))
    region = db.Column(db.String)
    city = db.Column(db.String)


class University(db.Model):
    __table_name__ = 'university'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


def populate_university():
    return _populate_table(University, open(db.get_app().config['ORGMEPHI_UNIVERSITY_FILE']).read().splitlines())


class Country(db.Model):
    __table_name__ = 'country'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


def populate_country():
    return _populate_table(Country, open(db.get_app().config['ORGMEPHI_COUNTRY_FILE']).read().splitlines())


if __name__ == "__main__":
    db.create_all()
