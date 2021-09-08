import enum
from sqlalchemy.ext.hybrid import hybrid_property

from common import get_current_db, get_current_app
from .auth import User
from user.util import admission_to_grade, grade_to_admission, get_unfilled
from .location import Location

db = get_current_db()
app = get_current_app()


class SchoolType(enum.Enum):
    school = 'School'
    lyceum = 'Lyceum'
    gymnasium = 'Gymnasium'
    education_center = 'EducationCenter'
    night_school = 'NightSchool'
    technical = 'Technical'
    external = 'External'
    collage = 'Collage'
    prof_tech = 'ProfTech'
    university = 'University'  # ?!
    correctional = 'Correctional'
    other = 'Other'


class SchoolInfo(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey(Location.id))
    school_type = db.Column(db.Enum(SchoolType))
    number = db.Column(db.Integer)
    name = db.Column(db.String)
    admission_year = db.Column(db.Date)
    user = db.relationship('User', back_populates='school_info')
    location = db.relationship('Location', lazy='select', uselist=False, single_parent=True,
                               cascade='save-update, merge, delete, delete-orphan')

    @hybrid_property
    def grade(self):
        return admission_to_grade(self.admission_year)

    @grade.setter
    def grade(self, value):
        self.admission_year = grade_to_admission(value)

    _required_fields = ['school_type', 'number', 'name', 'admission_year', 'location']

    def unfilled(self):
        return get_unfilled(self, self._required_fields, ['location'])
