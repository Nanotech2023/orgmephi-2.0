import datetime

from . import *

PARTICIPANT_NUM = 5


def step_school_register(client, state):
    requests = [{'username': f'participant {i}', 'password': 'qwertyA*1'} for i in range(PARTICIPANT_NUM)]
    responses = [client.post('/user/admin/internal_register', json=request) for request in requests]
    for response in responses:
        assert response.status_code == 200
    state.participants = [{'id': response.json['id'],
                           'username': response.json['username'],
                           'password': 'qwertyA*1'} for response in responses]


def step_personal_info(client, state):
    for user in state.participants:
        resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
        assert resp.status_code == 200

        user_id = user['id']

        date_of_birth = datetime.date.today() - datetime.timedelta(days=(100 * user['id'] + 365 * 16))

        if user_id % 4 == 3:
            document = {
                "code": f"{user_id % 10}{(user_id + 1) % 10}{(user_id + 2) % 10}-"
                        f"{(user_id + 3) % 10}{(user_id + 4) % 10}{(user_id + 5) % 10}",
                "document_type": "RFPassport",
                "issue_date": (date_of_birth + datetime.timedelta(days=(365 * 14))).isoformat(),
                "issuer": f"issuer {user_id}",
                "number": f"{user_id % 10}{(user_id + 1) % 10}{(user_id + 2) % 10}"
                          f"{(user_id + 3) % 10}{(user_id + 4) % 10}{(user_id + 5) % 10}",
                "series": f"45{(date_of_birth + datetime.timedelta(days=(365 * 14))).year % 100}"
            }
        elif user_id % 4 == 2:
            document = {
                "document_type": "RFInternationalPassport",
                "issue_date": (date_of_birth + datetime.timedelta(days=(365 * 14))).isoformat(),
                "issuer": f"issuer {user_id}",
                "number": f"{user_id % 10}{(user_id + 1) % 10}{(user_id + 2) % 10}"
                          f"{(user_id + 3) % 10}{(user_id + 4) % 10}{(user_id + 5) % 10}{(user_id + 6) % 10}",
                "series": f"{user_id % 10}{user_id + 1 % 10}"
            }
        elif user_id % 4 == 1:
            document = {
                "document_type": "ForeignPassport",
                "issue_date": (date_of_birth + datetime.timedelta(days=(365 * 14))).isoformat(),
                "issuer": f"issuer {user_id}",
                "number": f"{user_id % 10}{(user_id + 1) % 10}{(user_id + 2) % 10}"
                          f"{(user_id + 3) % 10}{(user_id + 4) % 10}{(user_id + 5) % 10}{(user_id + 6) % 10}",
                "series": f"{user_id % 10}{(user_id + 1) % 10}{(user_id + 2) % 10}{(user_id + 3) % 10}",
            }
        else:
            document = {
                "document_name": f"document {user_id}",
                "document_type": "OtherDocument",
                "issue_date": (date_of_birth + datetime.timedelta(days=(365 * 14))).isoformat(),
                "issuer": f"issuer {user_id}",
                "number": f"{user_id % 10}{(user_id + 1) % 10}{(user_id + 2) % 10}"
                          f"{(user_id + 3) % 10}{(user_id + 4) % 10}{(user_id + 5) % 10}{(user_id + 6) % 10}",
                "series": f"{user_id % 10}{(user_id + 1) % 10}{(user_id + 2) % 10}{(user_id + 3) % 10}",
            }

        if user_id % 2 == 1:
            dwelling = {
                'city': {'name': state.city['name'], 'region_name': state.city['region']},
                'country': state.country_native['name'],
                'rural': (user_id * 13 % 7) % 2
            }
        else:
            dwelling = {
                'country': state.country_foreign['name'],
                'location': f'location {user_id}',
                'rural': (user_id * 13 % 7) % 2
            }

        request = {
            "date_of_birth": date_of_birth.isoformat(),
            "document": document,
            "dwelling": dwelling,
            "email": f"user{user_id}@example.com",
            "first_name": f"user {user_id}",
            "gender": "Male" if (user_id * 13 % 17) % 2 else 'Female',
            "limitations": {
                "hearing": (user_id * 17 % 5) % 2,
                "movement": (user_id * 13 % 5) % 2,
                "sight": (user_id * 17 % 7) % 2
            },
            "middle_name": f"user {user_id}",
            "phone": f"8 (800) 555 {user_id % 10}{(user_id + 1) % 10} {(user_id + 2) % 10}{(user_id + 3) % 10}",
            "place_of_birth": f"place {user_id}",
            "second_name": f"user {user_id}"
        }

        resp = client.patch('/user/profile/personal', json=request)
        assert resp.status_code == 200

        user['personal'] = request

        resp = client.logout('/user/auth/logout')
        assert resp.status_code == 200


def step_school_info(client, state):
    for user in state.participants:
        resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
        assert resp.status_code == 200

        user_id = user['id']

        school_types = ['School', 'Lyceum', 'Gymnasium', 'EducationCenter', 'NightSchool', 'Technical', 'External',
                        'Collage', 'ProfTech', 'University', 'Correctional', 'Other']

        request = {
            "grade":
                datetime.date.today().year - datetime.date.fromisoformat(user['personal']['date_of_birth']).year - 7,
            "location": user['personal']['dwelling'],
            "name": f"school {user_id}",
            "number": user_id,
            "school_type": school_types[user_id % len(school_types)]
        }

        resp = client.patch('/user/profile/school', json=request)
        assert resp.status_code == 200

        user['school'] = request

        resp = client.logout('/user/auth/logout')
        assert resp.status_code == 200


steps_register_participants = [step_school_register, step_personal_info, step_school_info]
