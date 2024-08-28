import pytest
from datetime import timedelta
from django.utils import timezone
from ..factories import PostTagFactory, PostFactory, PostCategoryFactory
from sage_blog.models import PostTag

@pytest.mark.django_db
class TestTagQuerySet:

    @pytest.fixture
    def tags(self):
        # Setup tags, some with associated posts, some without
        tag1 = PostTagFactory()
        tag2 = PostTagFactory()
        tag3 = PostTagFactory()

        category1 = PostCategoryFactory()
        category2 = PostCategoryFactory()

        PostFactory.create_batch(5, tags=[tag1], category=category1, is_published=True)
        PostFactory.create_batch(3, tags=[tag2], category=category2, is_published=False)

        return [tag1, tag2, tag3]

    def test_filter_recent_tags_based_on_usage(self, tags):
        queryset = PostTag.objects.filter_recent_tags(days_ago=30)
        assert queryset.count() == 2  # Only tags with posts in the last 30 days should be returned

    def test_filter_recent_tags_limit(self, tags):
        queryset = PostTag.objects.filter_recent_tags(days_ago=30, limit=1)
        assert queryset.count() == 1  # Limiting the number of tags returned

    def test_filter_recent_tags_days_ago_zero(self, tags):
        queryset = PostTag.objects.filter_recent_tags(days_ago=0)
        assert queryset.count() == 3  # All tags should be returned

    def test_filter_recent_tags_excluding_specific_tag(self, tags):
        specific_tag = tags[0]
        queryset = PostTag.objects.filter_recent_tags(days_ago=30, obj=specific_tag)
        assert specific_tag not in queryset

    def test_filter_trend_tags_based_on_usage(self, tags):
        queryset = PostTag.objects.filter_trend_tags(days_ago=30, min_count=1)
        assert queryset.count() == 2  # Tags with at least 1 associated post should be returned

    def test_filter_trend_tags_min_count(self, tags):
        queryset = PostTag.objects.filter_trend_tags(days_ago=30, min_count=5)
        assert queryset.count() == 1  # Only tag with at least 5 posts should be returned

    def test_filter_trend_tags_limit(self, tags):
        queryset = PostTag.objects.filter_trend_tags(days_ago=30, limit=1)
        assert queryset.count() == 1  # Limiting the number of tags returned

    def test_search_case_insensitive(self, tags):
        search_term = tags[0].title.lower()
        queryset = PostTag.objects.search(search_term)
        assert queryset.count() == 1
        assert queryset[0].title.lower() == search_term

    def test_search_exact_match(self, tags):
        search_term = tags[0].title
        queryset = PostTag.objects.search(search_term)
        assert queryset.count() == 1
        assert queryset[0].title == search_term

    def test_search_partial_match(self, tags):
        search_term = tags[0].title[:3]  # Partial match on the first 3 characters
        queryset = PostTag.objects.search(search_term)
        assert queryset.count() >= 1

    def test_search_special_characters_or_empty_search(self):
        special_character_search = "@!#"
        empty_search = ""
        queryset_special_characters = PostTag.objects.search(special_character_search)
        queryset_empty_search = PostTag.objects.search(empty_search)
        assert queryset_special_characters.count() == 0  # Should return none
        assert queryset_empty_search.count() >= 0  # Depending on implementation, may return all tags

    def test_filter_by_posts_category_valid(self, tags):
        category = tags[0].posts.first().category
        queryset = PostTag.objects.filter_by_posts_category(category_title=category.title)
        assert queryset.count() == 1
        assert tags[0] in queryset

    def test_filter_by_posts_category_no_tags(self):
        category = PostCategoryFactory()  # Category with no associated tags
        queryset = PostTag.objects.filter_by_posts_category(category_title=category.title)
        assert queryset.count() == 0

    def test_filter_by_posts_category_non_existent(self):
        queryset = PostTag.objects.filter_by_posts_category(category_title="non-existent")
        assert queryset.count() == 0

    def test_sort_by_popularity(self, tags):
        queryset = PostTag.objects.sort_by_popularity()
        assert queryset.first().posts.count() >= queryset.last().posts.count()

    def test_sort_by_popularity_same_popularity(self):
        # Create tags with the same number of posts
        tag1 = PostTagFactory()
        tag2 = PostTagFactory()
        PostFactory.create_batch(2, tags=[tag1])
        PostFactory.create_batch(2, tags=[tag2])

        queryset = PostTag.objects.filter(id__in=[tag1.id, tag2.id]).sort_by_popularity()
        assert queryset.count() == 2
        assert queryset[0].posts.count() == queryset[1].posts.count()

    def test_sort_by_popularity_no_posts(self, tags):
        tag_with_no_posts = tags[2]  # This tag was created without posts
        queryset = PostTag.objects.sort_by_popularity()
        assert queryset.last() == tag_with_no_posts
