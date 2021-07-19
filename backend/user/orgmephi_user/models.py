from orgmephi_user import db
from datetime import datetime


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
    role = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    tmppassword_hash = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student_info.id'))


_roles = ['User', 'Creator', 'Admin']
_roles_maxlen = len(max(_roles, key=len))


class Role(db.Model):
    __table_name__ = 'role'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(_roles_maxlen), nullable=False, unique=True)


def populate_role():
    return _populate_table(Role, _roles)


class UserInfo(db.Model):
    __table_name__ = 'user_info'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    middle_name = db.Column(db.String, nullable=False)
    second_name = db.Column(db.String, nullable=False)
    dateofbirth = db.Column(db.Date, nullable=False)


class StudentInfo(db.Model):
    __table_name__ = 'student_info'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    phone = db.Column(db.String, nullable=False)
    university = db.Column(db.Integer, db.ForeignKey('university.id'))
    custom_university = db.Column(db.String)
    admission_year = db.Column(db.Date, nullable=False)
    university_country = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    citizenship = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    region = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)


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
