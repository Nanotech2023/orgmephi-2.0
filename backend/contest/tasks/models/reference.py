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
def populate_country():
    """
     pre-populate known target classes table with predefined values
    """
    from common.util import db_populate
    file_name = db.get_app().config.get('ORGMEPHI_TARGET_CLASSES_FILE', None)
    if file_name is not None:
        target_classes = open(file_name, encoding='utf8').read().splitlines()
        db_populate(db.session,
                    TargetClass, [TargetClass(target_class=target_class) for target_class in target_classes],
                    'target_class')
        db.session.commit()
