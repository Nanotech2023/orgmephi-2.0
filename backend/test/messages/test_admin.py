from . import *


@pytest.fixture
def client(client_admin):
    client_admin.set_prefix('/messages/admin')
    yield client_admin


def test_add_category(client):
    from messages.models import ThreadCategory
    request = {'name': 'Test'}
    resp = client.post('/add_category', json=request)
    assert resp.status_code == 204
    category = ThreadCategory.query.filter_by(name='Test').one_or_none()
    assert category is not None


def test_add_same_category(client, test_thread_categories):
    request = {'name': test_thread_categories[0].name}
    resp = client.post('/add_category', json=request)
    assert resp.status_code == 409


def test_delete_category(client, test_thread_categories):
    from messages.models import ThreadCategory
    category_name = test_thread_categories[0].name
    resp = client.post(f'/delete_category/{category_name}')
    assert resp.status_code == 204
    category = ThreadCategory.query.filter_by(name=category_name).one_or_none()
    assert category is None


def test_delete_thread(client, test_threads):
    from messages.models import Thread
    thr = test_threads[0]
    resp = client.post(f'/delete_thread/{thr.id}')
    assert resp.status_code == 204
    thread = Thread.query.filter_by(id=thr.id).one_or_none()
    assert thread is None


def test_cleanup_threads(client, test_threads):
    from messages.models import Thread
    threads_resolved = sorted([v for v in test_threads if v.resolved], key=lambda thr: thr.post_time)
    threads_unresolved = [v for v in test_threads if not v.resolved]
    request = {
        'amount': int(len(threads_resolved) / 2),
        'delete_unresolved': False
    }
    threads_resolved = threads_resolved[int(len(threads_resolved) / 2):]
    resp = client.post(f'/cleanup', json=request)
    assert resp.status_code == 204
    threads = Thread.query.all()
    assert set(threads) == set(threads_unresolved) | set(threads_resolved)


def test_cleanup_threads_unresolved(client, test_threads):
    from messages.models import Thread
    test_threads = sorted(test_threads, key=lambda thr: thr.post_time)
    request = {
        'amount': int(len(test_threads) / 2),
        'delete_unresolved': True
    }
    test_threads = test_threads[int(len(test_threads) / 2):]
    resp = client.post(f'/cleanup', json=request)
    assert resp.status_code == 204
    threads = Thread.query.all()
    assert set(threads) == set(test_threads)


def test_cleanup_threads_none(client, test_threads):
    from messages.models import Thread
    request = {
        'amount': 0,
        'delete_unresolved': True
    }
    resp = client.post(f'/cleanup', json=request)
    assert resp.status_code == 204
    threads = Thread.query.all()
    assert set(threads) == set(test_threads)
