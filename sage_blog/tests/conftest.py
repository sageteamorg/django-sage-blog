# sage_blog/tests/conftest.py

import pytest
from .factories import PostCategoryFactory, PostTagFactory, PostFactory, PostFaqFactory

@pytest.fixture
def category():
    return PostCategoryFactory()

@pytest.fixture
def tag():
    return PostTagFactory()

@pytest.fixture
def post(category, tag):
    return PostFactory(category=category, tags=[tag])

@pytest.fixture
def multiple_categories():
    return PostCategoryFactory.create_batch(5)

@pytest.fixture
def multiple_tags():
    return PostTagFactory.create_batch(10)

@pytest.fixture
def multiple_posts(multiple_categories, multiple_tags):
    posts = []
    for category in multiple_categories:
        posts.append(PostFactory(category=category, tags=multiple_tags))
    return posts

@pytest.fixture
def faq(post):
    return PostFaqFactory(post=post)

@pytest.fixture
def multiple_faqs(multiple_posts):
    faqs = []
    for post in multiple_posts:
        faqs.append(PostFaqFactory(post=post))
    return faqs
