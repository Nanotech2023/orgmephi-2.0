"""Database models of user management service."""

from orgmephi_user import db
from datetime import datetime
import enum
import sqlalchemy.exc


class UserRoleEnum(enum.Enum):
    """
        User roles enumeration class.

        user: common user
        creator: user with access to task management
        admin: administrator user
        system: may be used for maintenance or by connected services
    """
    participant = 'Participant'
    creator = 'Creator'
    admin = 'Admin'
    system = 'System'


class UserTypeEnum(enum.Enum):
    """
        User types enumeration class.

        pre_university: for admissions to the pre-university school
        enrollee: for admissions to the university
        school: participant of contests for school students
        university: participant of contests for university students
        internal: internal MEPhI user (e.g. creator or admin)
        pre_register: unconfirmed preregistered account
    """
    pre_university = 'PreUniversity'
    enrollee = 'Enrollee'
    school = 'School'
    university = 'University'
    internal = 'Internal'
    pre_register = 'PreRegister'


def _populate_table(table, values):
    """
        Populate a table with predefined values

        Parameters:

        table (class): ORM class of the table
        values (list): list of predefined values
    """
    for value in values:
        q = db.session.query(table).filter(table.name == value)
        if not db.session.query(q.exists()).scalar():
            instance = table(name=value)
            db.session.add(instance)
    db.session.commit()


class User(db.Model):
    """
        User ORM class

        Attributes:

        id: id of the user
        username: username of the user (email for external users, registration number for preregistered users)
        password_hash: hash sum of user's password
        role: user's role
        type: account type
        registration_date: date of registration
        user_id: id of corresponding personal info
        student_id: id of corresponding university student info
    """

    __table_name__ = 'user'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.Enum(UserRoleEnum), nullable=False)
    type = db.Column(db.Enum(UserTypeEnum), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    userInfo = db.relationship('UserInfo', backref='user', lazy=True, uselist=False)
    studentInfo = db.relationship('StudentInfo', backref='user', lazy=True, uselist=False)


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

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    email = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    second_name = db.Column(db.String)
    date_of_birth = db.Column(db.Date)


class StudentInfo(db.Model):
    """
        University student info ORM class

        Attributes:

        id: id of the info
        phone: user's phone number
        university: id of student's university from known university list
        custom_university: name of student's university if the university is not in the known university list
        admission_year: year of admission to the university
        university_country: country of the university
        citizenship: student's citizenship
        region: student's country region
        city: student's city
    """

    __table_name__ = 'student_info'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    phone = db.Column(db.String)
    university = db.Column(db.Integer, db.ForeignKey('university.id'))
    custom_university = db.Column(db.String)
    admission_year = db.Column(db.Date)
    university_country = db.Column(db.Integer, db.ForeignKey('country.id'))
    citizenship = db.Column(db.Integer, db.ForeignKey('country.id'))
    region = db.Column(db.String)
    city = db.Column(db.String)


class University(db.Model):
    """
        Known universities ORM class

        Attributes:

        id: id of the university
        name: name of the university
    """
    __table_name__ = 'university'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


def populate_university():
    """
    pre-populate known university table with predefined values
    """
    return _populate_table(University, open(db.get_app().config['ORGMEPHI_UNIVERSITY_FILE']).read().splitlines())


class Country(db.Model):
    """
        Known countries ORM class

        Attributes:

        id: id of the country
        name: name of the country
    """
    __table_name__ = 'country'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


def populate_country():
    """
     pre-populate known country table with predefined values
    """
    return _populate_table(Country, open(db.get_app().config['ORGMEPHI_COUNTRY_FILE']).read().splitlines())


# Many-To-Many relationship for User <-> Group
users_in_group = db.Table('user_in_group',
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                          db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
                          )


class Group(db.Model):
    """
        Group ORM class

        Attributes:

        id: id of the group
        name: name of the group
        users: relationship with users within the group
    """
    __table_name__ = 'group'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    users = db.relationship('User', secondary=users_in_group, lazy='subquery',
                            backref=db.backref('group', lazy=True))


def add_user(db_session, username, password_hash, role, reg_type):
    from orgmephi_user.errors import AlreadyExists
    user = User(
        username=username,
        password_hash=password_hash,
        role=role,
        type=reg_type
    )
    db_session.add(user)

    try:
        db_session.flush()
    except sqlalchemy.exc.IntegrityError:
        raise AlreadyExists('username', username)
    return user


def get_user_by_name(username):
    return User.query.filter(User.username == username).one_or_none()


def add_personal_info(db_session, user, email, first_name, second_name, middle_name, date_of_birth):
    user_info = UserInfo(
        user_id=user.id,
        email=email,
        first_name=first_name,
        second_name=second_name,
        middle_name=middle_name,
        date_of_birth=date_of_birth
    )
    db_session.add(user_info)
    db_session.flush()


def add_university_info(db_session, user, phone, university_name, admission_year, university_country, citizenship,
                        region, city):
    university = University.query.filter(University.name == university_name).one_or_none()
    student_info = StudentInfo(
        user_id=user.id,
        phone=phone,
        university=(university.id if university is not None else None),
        custom_university=(university_name if university is None else None),
        admission_year=admission_year,
        university_country=university_country,
        citizenship=citizenship,
        region=region,
        city=city
    )
    db_session.add(student_info)
    db_session.flush()
    return student_info


if __name__ == "__main__":
    db.create_all()
