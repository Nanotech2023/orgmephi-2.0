from . import *


def step_browse_news(client, state):
    resp = client.get('/news/visitor/news')
    assert resp.status_code == 200

    news_id = resp.json['news'][0]['id']

    resp = client.get(f'/news/visitor/news/{news_id}')
    assert resp.status_code == 200
    assert len(resp.json['title']) > 0
    assert len(resp.json['body']) > 0

    resp = client.get(f'/news/visitor/news/{news_id}/image')
    assert resp.status_code == 200
    assert len(resp.data) > 0


steps_browse_news = [step_browse_news]
