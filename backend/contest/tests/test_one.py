import pytest

from contest_data.models_tasks import Task


def test_one(flask_init):

    db = flask_init
    re = Task.query.all()
    for p in re:
        db.session.delete(p)

    print("I'm here!")
    db = flask_init
    r = Task(num_of_task=1)
    db.session.add(r)
    db.session.commit()
    re = Task.query.all()
    print(re[0].num_of_task)
    assert len(re) == 1
    # print(db.engine.table_names())
    re = Task.query.all()
    for p in re:
        db.session.delete(p)
    db.session.commit()
