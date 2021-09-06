from . import *


def test_add_category(client_admin):
    from news.models import NewsCategory

    request = {'name': 'Test category create'}
    resp = client_admin.post('/admin/add_category', json=request)
    assert resp.status_code == 200
    assert resp.json['name'] == 'Test category create'
    assert test_app.db.session.query(NewsCategory.query.filter_by(name='Test category create').exists()).scalar()


def test_add_category_exists(client_admin):
    request = {'name': 'Test category create'}
    client_admin.post('/admin/add_category', json=request)
    resp = client_admin.post('/admin/add_category', json=request)
    assert resp.status_code == 409


def test_delete_category(client_admin):
    from news.models import NewsCategory

    request = {'name': 'Test category create'}
    client_admin.post('/admin/add_category', json=request)
    resp = client_admin.post('/admin/delete_category/Test category create', json=request)
    assert resp.status_code == 204
    assert not test_app.db.session.query(NewsCategory.query.filter_by(name='Test category create').exists()).scalar()


def test_delete_news(client_admin, test_news):
    from news.models import News

    news = test_news[0]

    resp = client_admin.post(f'/admin/news/{news.id}/delete')
    assert resp.status_code == 204
    assert not test_app.db.session.query(News.query.filter_by(id=news.id).exists()).scalar()
