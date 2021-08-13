from common import get_current_db, get_current_app
from datetime import datetime
import enum

db = get_current_db()
app = get_current_app()


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


# Many-To-Many relationship for User <-> Group
users_in_group = db.Table('user_in_group',
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                          db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
                          )


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

    user_info = db.relationship('UserInfo', back_populates='user', lazy=True, uselist=False,
                                cascade='save-update, merge, delete, delete-orphan')
    student_info = db.relationship('StudentInfo', back_populates='user', lazy=True, uselist=False,
                                   cascade='save-update, merge, delete, delete-orphan')
    groups = db.relationship('Group', secondary=users_in_group, lazy='select', back_populates='users')


def add_user(db_session, username, password_hash, role, reg_type):
    from .personal import UserInfo
    from .university import StudentInfo
    user = User(
        username=username,
        password_hash=password_hash,
        role=role,
        type=reg_type
    )
    user.user_info = UserInfo()
    user.student_info = StudentInfo()
    db_session.add(user)
    return user


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

    users = db.relationship('User', secondary=users_in_group, lazy='subquery', back_populates='groups')
