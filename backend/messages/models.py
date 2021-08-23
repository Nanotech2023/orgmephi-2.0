from common import get_current_db, get_current_app
from datetime import datetime
import enum

from sqlalchemy.ext.hybrid import hybrid_property

from user.models import User
from contest.tasks.models import Contest
from contest.responses.models import Response, Appeal

db = get_current_db()
app = get_current_app()


class ThreadType(enum.Enum):
    appeal = 'Appeal'
    work = 'Work'
    contest = 'Contest'
    general = 'General'


class ThreadStatus(enum.Enum):
    open = 'Open'
    closed = 'Closed'
    accepted = 'Accepted'
    rejected = 'Rejected'


class ThreadCategory(db.Model):
    name = db.Column(db.String, primary_key=True)


class Thread(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    category_name = db.Column(db.String, db.ForeignKey(ThreadCategory.name), nullable=False)
    thread_type = db.Column(db.Enum(ThreadType), nullable=False)

    resolved = db.Column(db.Boolean, default=False, index=True, nullable=False)
    status = db.Column(db.Enum(ThreadStatus), default=ThreadStatus.open, nullable=False)

    post_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    resolve_time = db.Column(db.DateTime)

    topic = db.Column(db.String, nullable=False)

    related_contest_id = db.Column(db.Integer, db.ForeignKey(Contest.contest_id))
    related_work_id = db.Column(db.Integer, db.ForeignKey(Response.work_id))
    related_appeal_id = db.Column(db.Integer, db.ForeignKey(Appeal.appeal_id))

    messages = db.relationship('Message', back_populates='thread', lazy=True, uselist=True,
                               cascade='save-update, merge, delete, delete-orphan', order_by='Message.post_time')

    author = db.relationship('User')

    category = db.relationship('ThreadCategory')

    related_contest = db.relationship('Contest')
    related_work = db.relationship('Response')
    related_appeal = db.relationship('Appeal')

    @hybrid_property
    def answered(self):
        if not self.messages:
            return False
        return self.messages[-1].from_mephi


class Message(db.Model):
    message_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey(Thread.id), nullable=False)

    post_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    from_mephi = db.Column(db.Boolean, nullable=False)

    message = db.Column(db.String, nullable=False)

    thread = db.relationship('Thread', back_populates='messages', lazy=True, uselist=False)


if __name__ == "__main__":
    get_current_db().create_all()
