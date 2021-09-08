from . import *


@pytest.fixture
def client(client_creator):
    client_creator.set_prefix('responses/creator')
    yield client_creator


def test_user_response(client, create_plain_task):
    contest_id = get_contest_id(create_plain_task)
    user_id = get_user_id(create_plain_task)
    resp = client.post(f'/contest/{contest_id}/user/{1000}/create')
    assert resp.status_code == 404

    resp = client.post(f'/contest/{contest_id}/user/{user_id}/create')
    assert resp.status_code == 200

    resp = client.post(f'/contest/{contest_id}/user/{user_id}/create')
    assert resp.status_code == 409

    from contest.responses.util import get_user_in_contest_work
    response = get_user_in_contest_work(user_id, contest_id)
    assert response.work_status.value == 'InProgress'

