from . import *

def step_create_categories(client, state):
    resp = client.login('/user/auth/login', username=state.admin['username'], password=state.admin['password'])
    assert resp.status_code == 200

    news_categories = ['Olympiad', 'Maintenance', 'Other']
    for category in news_categories:
        resp = client.post('/news/admin/add_category', json={'name': category})
        assert resp.status_code == 200

    client.logout('/user/auth/logout')

    state.news_categories = news_categories
    state.news_category_olympiad = 'Olympiad'


def step_create_news(client, state):
    from contest.tasks.models import Contest
    resp = client.login('/user/auth/login', username=state.creator['username'], password=state.creator['password'])
    assert resp.status_code == 200

    contest = Contest.query.filter_by(contest_id=state.contest['contest_id']).one_or_none()

    request = \
        {
            'category': state.news_category_olympiad,
            'title': f'Olympiad {contest.base_contest.name}',
            'body': f'Olympiad {contest.base_contest.name} of {contest.academic_year} starting soon. Participate in '
                    f'{contest.base_contest.subject.value} contest on {contest.start_date.isoformat()}!',
            'related_contest': contest.contest_id
        }

    resp = client.post('/news/creator/news', json=request)
    assert resp.status_code == 200
    state.news = {'id': resp.json['id']}

    resp = client.post(f'/news/creator/news/{state.news["id"]}/image', data=test_image, mimetype='image/jpg')
    assert resp.status_code == 204

    resp = client.post(f'/news/creator/news/{state.news["id"]}/post')
    assert resp.status_code == 204

    client.logout('/user/auth/logout')


steps_create_news = [step_create_categories, step_create_news]