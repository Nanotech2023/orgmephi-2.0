from datetime import date, datetime


def update_password(user_id, new_password, old_password, admin=False):
    from common import get_current_app, get_current_db
    from common.util import db_get_or_raise
    from .models import User
    from flask import make_response

    app = get_current_app()
    db = get_current_db()

    user = db_get_or_raise(User, "id", user_id)
    if not admin:
        app.password_policy.validate_password(old_password, user.password_hash)
    password_hash = app.password_policy.hash_password(new_password, check=not admin)
    user.password_hash = password_hash
    user.password_changed = datetime.utcnow()
    db.session.commit()
    return make_response({}, 200)


def year_admission(year):
    return date(year, 9, 1)


def admission_date(from_date):
    admission = year_admission(from_date.year)
    if from_date < admission:
        admission = year_admission(from_date.year - 1)
    return admission


def grade_to_admission(grade):
    last_admission = admission_date(datetime.utcnow().date())
    return date(last_admission.year - grade + 1, last_admission.month, last_admission.day)


def admission_to_grade(admission):
    return admission_date(datetime.utcnow().date()).year - admission.year + 1


def get_unfilled(obj, required_fields: list[str], child_fields: list[str]):
    unfilled = [key for key in required_fields if getattr(obj, key, None) is None]
    for key in child_fields:
        attr = getattr(obj, key, None)
        if attr is not None:
            unfilled_attr = attr.unfilled()
            if len(unfilled_attr) > 0:
                unfilled.append({key: unfilled_attr})
    return unfilled


def get_username_case_insensitive(email):
    from sqlalchemy import func
    from user.models import User
    return User.query.filter(func.lower(User.username) == func.lower(email)).one_or_none()


def get_email_case_insensitive_or_none(email):
    from sqlalchemy import func
    from user.models import UserInfo
    return UserInfo.query.filter(func.lower(UserInfo.email) == func.lower(email)).one_or_none()


def get_email_case_insensitive_or_raise(email):
    from common.errors import NotFound
    user = get_email_case_insensitive_or_none(email)
    if user is None:
        raise NotFound('email', str(email))
    return user
