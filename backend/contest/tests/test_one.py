import pytest

from contest_data.models_responses import Response


def test_one(flask_init):
    print("I'm here!")
    db = flask_init
    r = Response(user_id=1, contest_id=1)
    db.session.add(r)
    db.session.commit()
    re = Response.query.all()
    print(re[0].user_id)
    assert len(re) == 1
    re = Response.query.all()
    for p in re:
        db.session.delete(p)
    db.session.commit()
