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
    university = db.Column(db.Integer, db.ForeignKey(University.id))
    custom_university = db.Column(db.String)
    admission_year = db.Column(db.Date)
    university_country_id = db.Column(db.Integer, db.ForeignKey(Country.id))
    citizenship_country_id = db.Column(db.Integer, db.ForeignKey(Country.id))
    region = db.Column(db.String)
    city = db.Column(db.String)

    user = db.relationship('User', back_populates='student_info', lazy='select')
