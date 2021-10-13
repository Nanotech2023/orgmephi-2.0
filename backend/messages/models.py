from common import get_current_db, get_current_app
from datetime import datetime
import enum

from sqlalchemy import func, select
from sqlalchemy.sql import case
from sqlalchemy.ext.hybrid import hybrid_property

from user.models import User
from contest.tasks.models import Contest

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

    messages = db.relationship('Message', back_populates='thread', lazy=True, uselist=True,
                               cascade='save-update, merge, delete, delete-orphan', order_by='Message.post_time')

    author = db.relationship('User')

    category = db.relationship('ThreadCategory')

    related_contest = db.relationship('Contest')

    @hybrid_property
    def author_username(self):
        return getattr(self.author, 'username', None)

    @hybrid_property
    def author_first_name(self):
        return getattr(getattr(self.author, 'user_info', None), 'first_name', None)

    @hybrid_property
    def author_second_name(self):
        return getattr(getattr(self.author, 'user_info', None), 'second_name', None)

    @hybrid_property
    def author_middle_name(self):
        return getattr(getattr(self.author, 'user_info', None), 'middle_name', None)

    @hybrid_property
    def answered(self):
        if not self.messages:
            return False
        return self.messages[-1].employee_id is not None

    # noinspection PyMethodParameters
    @answered.expression
    def answered(cls):
        # noinspection PyComparisonWithNone,PyUnresolvedReferences
        return case([(select(func.count(Message.id) > 0).where(Message.thread_id == cls.id).scalar_subquery(),
                      select(Message.employee_id != None).where(Message.thread_id == cls.id).
                      order_by(Message.post_time.desc()).limit(1).scalar_subquery()
                      )], else_=False)

    @hybrid_property
    def update_time(self):
        if not self.messages:
            return self.post_time
        return self.messages[-1].post_time

    # noinspection PyMethodParameters
    @update_time.expression
    def update_time(cls):
        # noinspection PyUnresolvedReferences
        return case([(select(func.count(Message.id) > 0).where(Message.thread_id == cls.id).scalar_subquery(),
                      select(Message.post_time).where(Message.thread_id == cls.id).
                      order_by(Message.post_time.desc()).limit(1).scalar_subquery()
                      )], else_=cls.post_time)


class Message(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey(Thread.id), nullable=False)

    post_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)

    message = db.Column(db.String, nullable=False)

    thread = db.relationship('Thread', back_populates='messages', lazy=True, uselist=False)
    employee = db.relationship('User')


if __name__ == "__main__":
    get_current_db().create_all()
