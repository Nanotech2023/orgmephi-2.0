from datetime import datetime

# noinspection PyUnresolvedReferences
from .. import *
from ..responses import *


@pytest.fixture
def test_thread_categories():
    from messages.models import ThreadCategory
    categories = [ThreadCategory(name=f'Test category {i}') for i in range(4)]
    test_app.db.session.add_all(categories)
    test_app.db.session.commit()
    yield categories


@pytest.fixture
def test_threads(test_thread_categories, create_user_response):
    from messages.models import Thread, ThreadType, ThreadStatus
    thread_types = [v for v in ThreadType]
    thread_statuses = [v for v in ThreadStatus]
    responses = create_user_response['responses']
    threads = [Thread(author_id=responses[i % len(responses)].user_id,
                      category=test_thread_categories[i % len(test_thread_categories)],
                      thread_type=thread_types[i % len(thread_types)],
                      resolved=(i % 2),
                      status=thread_statuses[i % len(thread_types)],
                      topic=f'Test message {i}',
                      related_contest_id=responses[i % len(responses)].contest_id
                      ) for i in range(8)]
    for i in range(len(threads)):
        if threads[i].status != ThreadStatus.open:
            threads[i].resolve_time = datetime.utcnow()
    for i in range(len(threads)):
        if threads[i].status == ThreadStatus.closed and threads[i].thread_type == ThreadType.appeal:
            threads[i].status = ThreadStatus.accepted if i % 2 == 0 else ThreadStatus.rejected
    test_app.db.session.add_all(threads)
    test_app.db.session.commit()
    yield threads


@pytest.fixture
def test_messages(test_threads, test_user_creator):
    from messages.models import Message
    messages = [Message(thread=test_threads[i % len(test_threads)],
                        employee=test_user_creator,
                        message=f'Test message {i}',
                        ) for i in range(len(test_threads) * 3)]
    test_app.db.session.add_all(messages)
    test_app.db.session.commit()
    yield messages


# noinspection Assert
def cmp_thread(thread, json):
    assert json['id'] == thread.id
    assert json['author'] == thread.author_id
    assert json['category'] == thread.category_name
    assert json['thread_type'] == thread.thread_type.value
    assert json['resolved'] == thread.resolved
    assert json['status'] == thread.status.value
    assert json['post_time'] == thread.post_time.isoformat()
    assert json['topic'] == thread.topic
    assert json['related_contest'] == thread.related_contest_id
    if thread.resolved:
        assert json['resolve_time'] == thread.resolve_time.isoformat()


# noinspection Assert
def cmp_thread_list(thread_list, json):
    assert json['count'] == len(thread_list)
    assert len(json['threads']) == len(thread_list)
    for thread in thread_list:
        resp_thread = next((v for v in json['threads'] if v['id'] == thread.id))
        cmp_thread(thread, resp_thread)
