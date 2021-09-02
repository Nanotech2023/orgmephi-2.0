from .reference import *
from .personal import *
from .auth import *
from .university import *
from .school import *
from .location import *
from .document import *


def _year_admission(year):
    from datetime import date
    return date(year, 9, 1)


def _admission_date(from_date):
    admission = _year_admission(from_date.year)
    if from_date < admission:
        admission = _year_admission(from_date.year - 1)
    return admission


def _grade_to_admission(grade):
    from datetime import date, datetime
    last_admission = _admission_date(datetime.utcnow().date())
    return date(last_admission.year - grade + 1, last_admission.month, last_admission.day)


def _admission_to_grade(admission):
    from datetime import datetime
    return _admission_date(datetime.utcnow().date()).year - admission.year + 1


if __name__ == "__main__":
    get_current_db().create_all()
