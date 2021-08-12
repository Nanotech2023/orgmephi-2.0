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

    def serialize(self):
        if self.custom_university is None:
            university = University.query.filter(University.id == self.university).one_or_none().name
        else:
            university = self.custom_university
        return \
            {
                'phone_number': self.phone,
                'university': university,
                'admission_year': self.admission_year.isoformat(),
                'university_country': self.university_country,
                'citizenship': self.citizenship,
                'region': self.region,
                'city': self.city
            }

    def update(self, phone_number=None, university=None, admission_year=None, university_country=None,
               citizenship=None, region=None, city=None):
        if phone_number is not None:
            self.phone = phone_number
        if university is not None:
            university_obj = University.query.filter(University.name == university).one_or_none()
            if university_obj is None:
                self.university = None
                self.custom_university = university
            else:
                self.university = university_obj.id
                self.custom_university = None
        if admission_year is not None:
            self.admission_year = admission_year
        if university_country is not None:
            self.university_country = university_country
        if citizenship is not None:
            self.citizenship = citizenship
        if region is not None:
            self.region = region
        if city is not None:
            self.city = city


def create_university_info(phone, university_name, admission_year, university_country, citizenship,
                           region, city):
    university = University.query.filter(University.name == university_name).one_or_none()
    student_info = StudentInfo(
        phone=phone,
        university=(university.id if university is not None else None),
        custom_university=(university_name if university is None else None),
        admission_year=admission_year,
        university_country=university_country,
        citizenship=citizenship,
        region=region,
        city=city
    )
    return student_info
