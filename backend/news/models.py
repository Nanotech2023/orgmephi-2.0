from datetime import datetime

from common import get_current_db, get_current_app

from contest.tasks.models import Contest

db = get_current_db()
app = get_current_app()


class NewsCategory(db.Model):
    name = db.Column(db.String, primary_key=True)


class News(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String, db.ForeignKey(NewsCategory.name), nullable=False)
    post_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    posted = db.Column(db.Boolean, default=False, nullable=False)

    title = db.Column(db.String, nullable=False)
    image = db.Column(db.LargeBinary)
    body = db.Column(db.String)

    related_contest_id = db.Column(db.Integer, db.ForeignKey(Contest.contest_id))
    grade = db.Column(db.Integer)

    category = db.relationship('NewsCategory')
    related_contest = db.relationship('Contest')
