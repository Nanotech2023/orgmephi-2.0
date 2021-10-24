# noinspection PyUnresolvedReferences
import io

from common.media_types import NewsImage
from .. import *
from ..tasks import *  # Fixtures


@pytest.fixture
def test_categories():
    from news.models import NewsCategory
    categories = [NewsCategory(name=f'Test category {i}') for i in range(2)]
    test_app.db.session.add_all(categories)
    test_app.db.session.commit()
    yield categories


@pytest.fixture
def test_news(test_categories, test_contests):
    from news.models import News
    news = [News(title=f'Test news {i}', body=f'Test news {i}', posted=(i % 2 == 0),
                 category=test_categories[i % len(test_categories)], grade=(i % 4 + 8),
                 related_contest=test_contests[i % len(test_contests)]) for i in range(8)]
    for news_el in news:
        with test_app.store_manager:
            news_el.image = NewsImage.create_from(
                attachable=io.BytesIO(test_image),
                store_id=test_app.get_media_store_id('NEWS')
            )
    test_app.db.session.add_all(news)
    test_app.db.session.commit()
    yield news


@pytest.fixture
def test_news_posted(test_news):
    yield [v for v in test_news if v.posted]


@pytest.fixture
def test_news_not_posted(test_news):
    yield [v for v in test_news if not v.posted]


# noinspection Assert
def cmp_news(news, json, info=True):
    assert json['id'] == news.id
    assert json['category'] == news.category_name
    assert json['post_time'] == news.post_time.isoformat()
    assert json['posted'] == news.posted
    assert json['grade'] == news.grade
    assert json['title'] == news.title
    if info:
        assert 'body' not in json
    else:
        assert json['body'] == news.body


# noinspection Assert
def cmp_news_list(news_list, json, info=True):
    assert json['count'] == len(news_list)
    assert len(json['news']) == len(news_list)
    for news in news_list:
        resp_news = next((v for v in json['news'] if v['id'] == news.id))
        cmp_news(news, resp_news, info)
