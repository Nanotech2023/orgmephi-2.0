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
    db.session.commit()
    return make_response({}, 200)
