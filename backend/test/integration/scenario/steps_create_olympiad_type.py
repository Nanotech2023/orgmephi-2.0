from . import *


def step_create_olympiad_type(client, state):
    request = {'olympiad_type': 'Test type'}
    resp = client.post('contest/tasks/admin/olympiad_type/create', json=request)
    assert resp.status_code == 200
    state.olympiad_type = dict()
    state.olympiad_type['olympiad_type_id'] = resp.json['olympiad_type_id']
    state.olympiad_type['olympiad_type'] = 'Test type'


def step_create_olympiad_location(client, state):
    request = {'url': 'https://www.example.com'}
    resp = client.post('contest/tasks/admin/location/create_online', json=request)
    assert resp.status_code == 200
    state.olympiad_location = dict()
    state.olympiad_location['location_id'] = resp.json['location_id']
    state.olympiad_location['url'] = 'https://www.example.com'


steps_create_olympiad_type = [step_create_olympiad_type, step_create_olympiad_location]
