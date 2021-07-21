import pytest

from contest_data.models_tasks import Task, TaskVariant


def test_Task_1(flask_init):

    db = flask_init
    re = Task.query.all()
    for p in re:
        db.session.delete(p)
    print("Task model creation...")
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


def test_TaskVariant_1(flask_init):

    db = flask_init
    re = TaskVariant.query.all()
    for p in re:
        db.session.delete(p)

    print("Task variant creation...")
    db = flask_init
    r = TaskVariant(variant_number=1, variant_description='Test...')
    db.session.add(r)
    db.session.commit()
    re = TaskVariant.query.all()
    print(re[0].variant_number)
    assert len(re) == 1
    # print(db.engine.table_names())
    re = TaskVariant.query.all()
    for p in re:
        db.session.delete(p)
    db.session.commit()


def test_TaskVariant_2(flask_init):

    db = flask_init
    re = TaskVariant.query.all()
    for p in re:
        db.session.delete(p)

    print("Task variant creation...")
    db = flask_init
    r = TaskVariant(variant_number=1, variant_description='Test...')
    db.session.add(r)
    db.session.commit()
    re = TaskVariant.query.all()
    print(re[0].variant_number)
    assert len(re) == 1
    # print(db.engine.table_names())
    re = TaskVariant.query.all()
    for p in re:
        db.session.delete(p)
    db.session.commit()
