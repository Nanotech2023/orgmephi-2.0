from common import get_current_db, get_current_app

db = get_current_db()
app = get_current_app()


class TargetClass(db.Model):
    """
    Target class for contest

    target_class_id: target class_id
    target_class: target_class
    """

    __tablename__ = 'target_class'

    target_class_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    target_class = db.Column(db.Text, nullable=False)


@app.db_prepare_action()
def populate_target_classes():
    """
     pre-populate known target classes table with predefined values
    """
    from common.util import db_populate
    classes = [str(target_class) for target_class in range(8, 12)] + ['student']

    db_populate(db.session,
                TargetClass, [TargetClass(target_class=target_class) for target_class in classes],
                'target_class')
    db.session.commit()
