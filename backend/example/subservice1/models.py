from common import get_current_db

db = get_current_db()


class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def serialize(self):
        return {'id': self.id, 'name': self.name}
