from . import *


def step_admin_login(client, state):
    resp = client.login('/user/auth/login', username=state.admin['username'], password=state.admin['password'])
    assert resp.status_code == 200


def step_creator_register(client, state):
    request = {'username': 'creator', 'password': 'qwertyA*1'}
    resp = client.post('/user/admin/internal_register', json=request)
    assert resp.status_code == 200
    state.creator = dict()
    state.creator['id'] = resp.json['id']
    state.creator['username'] = resp.json['username']
    state.creator['password'] = 'qwertyA*1'


def step_creator_give_permissions(client, state):
    resp = client.put(f'/user/admin/role/{state.creator["id"]}', json={'role': 'Creator'})
    assert resp.status_code == 200


def step_creator_fill_personal(client, state):
    request = {
        "date_of_birth": "1981-09-16",
        "email": "iiivanov@mephi.ru",
        "first_name": "Иван",
        "second_name": "Иванов",
        "middle_name": "Иванович",
        "phone": "8 (800) 555 35 35"
    }
    resp = client.patch(f'/user/admin/personal/{state.creator["id"]}', json=request)
    assert resp.status_code == 200


steps_register_creator = [step_admin_login, step_creator_register, step_creator_give_permissions,
                          step_creator_fill_personal]
