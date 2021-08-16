from common import get_current_db, get_current_app
from .reference import University, Country
from .auth import User

db = get_current_db()
app = get_current_app()


class StudentInfo(db.Model):
    """
        University student info ORM class

        Attributes:

        id: id of the info
        phone: user's phone number
        university: id of student's university from known university list
        custom_university: name of student's university if the university is not in the known university list
        admission_year: year of admission to the university
        university_country_id: country of the university
        citizenship_country_id: student's citizenship
        region: student's country region
        city: student's city
    """

    __table_name__ = 'student_info'

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    phone = db.Column(db.String)
    admission_year = db.Column(db.Date)

    university = db.relationship('StudentUniversity', lazy='select', uselist=False,
                                 cascade='save-update, merge, delete, delete-orphan')

    user = db.relationship('User', lazy='select')


class StudentUniversity(db.Model):
    """
        Base ORM class for student -> university relationship
    """

    user_id = db.Column(db.Integer, db.ForeignKey(StudentInfo.user_id), primary_key=True)
    known = db.Column(db.Boolean)

    __mapper_args__ = {
        'with_polymorphic': '*',
        "polymorphic_on": known
    }


class StudentUniversityKnown(StudentUniversity):
    """
        ORM class for student -> known university relationship

        Attributes:

        university_id: id of student's university
    """

    university_id = db.Column(db.Integer, db.ForeignKey(University.id))
    university = db.relationship('University')

    @property
    def country(self):
        return "Not Implemented"

    __mapper_args__ = {
        'polymorphic_identity': True,
        'with_polymorphic': '*'
    }


class StudentUniversityCustom(StudentUniversity):
    """
        ORM class for student -> custom (unknown) university relationship

        Attributes:

        university: name of student's university
    """

    university_name = db.Column(db.String)
    university_country_name = db.Column(db.String, db.ForeignKey(Country.name))
    country = db.relationship('Country')

    __mapper_args__ = {
        'polymorphic_identity': False,
        'with_polymorphic': '*'
    }
