import pytest
from django.utils import timezone
from django.conf import settings
from datetime import timedelta

from ..factories import PostFactory, PostCategoryFactory, PostTagFactory
from sage_blog.models import Post


@pytest.mark.django_db
class TestPostQuerySet:

    @pytest.fixture
    def posts(self):
        category1 = PostCategoryFactory(slug="category-1")
        category2 = PostCategoryFactory(slug="category-2")
        tag1 = PostTagFactory(slug="tag-1")
        tag2 = PostTagFactory(slug="tag-2")

        posts = [
            PostFactory(is_published=True, category=category1, tags=[tag1]),
            PostFactory(is_published=False, category=category1, tags=[tag2]),
            PostFactory(is_published=True, category=category2, tags=[tag1]),
            PostFactory(is_published=True, category=category2, tags=[tag2]),
        ]
        return posts

    def test_filter_actives_all_published(self, posts):
        queryset = Post.objects.filter_actives(is_published=True)
        assert queryset.count() == 3

    def test_filter_actives_all_unpublished(self, posts):
        queryset = Post.objects.filter_actives(is_published=False)
        assert queryset.count() == 1

    def test_filter_actives_mix_published_unpublished(self, posts):
        queryset_published = Post.objects.filter_actives(is_published=True)
        queryset_unpublished = Post.objects.filter_actives(is_published=False)
        assert queryset_published.count() == 3
        assert queryset_unpublished.count() == 1

    def test_filter_actives_empty_post_list(self):
        queryset = Post.objects.all()
        queryset = queryset.filter_actives(is_published=True)
        assert queryset.count() == 0

    def test_filter_recent_posts_fewer_than_num_posts(self, posts):
        queryset = Post.objects.filter_recent_posts(num_posts=5)
        assert queryset.count() == 4

    def test_filter_recent_posts_exact_num_posts(self, posts):
        queryset = Post.objects.filter_recent_posts(num_posts=3)
        assert queryset.count() == 3

    def test_filter_recent_posts_excluding_specific_post(self, posts):
        specific_post = posts[0]
        queryset = Post.objects.filter_recent_posts(num_posts=3, obj=specific_post)
        assert queryset.count() == 3
        assert specific_post not in queryset

    def test_filter_recent_posts_empty_post_list(self):
        queryset = Post.objects.none().filter_recent_posts(num_posts=3)
        assert queryset.count() == 0

    def test_filter_by_category_valid_slug(self, posts):
        queryset = Post.objects.filter_by_category(category_slug=posts[0].category.slug)
        assert queryset.count() == 2
        for post in queryset:
            assert post.category.slug == posts[0].category.slug

    def test_filter_by_category_non_existent_slug(self):
        queryset = Post.objects.filter_by_category(category_slug="non-existent")
        assert queryset.count() == 0

    def test_filter_by_tag_valid_slug(self, posts):
        tags = [tag.slug for tag in posts[0].tags.all()]
        queryset = Post.objects.filter_by_tag(tag_slug=tags[0])
        assert queryset.count() == 2
        for post in queryset:
            assert any(tag.slug == tags[0] for tag in post.tags.all())

    def test_filter_by_tag_non_existent_slug(self):
        queryset = Post.objects.filter_by_tag(tag_slug="non-existent")
        assert queryset.count() == 0

    def test_filter_in_date_range_valid(self, posts):
        start_date = timezone.now() - timedelta(days=1)
        end_date = timezone.now() + timedelta(days=1)
        queryset = Post.objects.filter_in_date_range(start_date, end_date)
        assert queryset.count() == 4

    def test_filter_in_date_range_no_posts_in_range(self, posts):
        start_date = timezone.now() + timedelta(days=10)
        end_date = timezone.now() + timedelta(days=20)
        queryset = Post.objects.filter_in_date_range(start_date, end_date)
        assert queryset.count() == 0

    def test_filter_in_date_range_edge_cases(self, posts):
        start_date = timezone.now() - timedelta(days=1)
        end_date = timezone.now()
        queryset = Post.objects.filter_in_date_range(start_date, end_date)
        assert queryset.count() == 4

    def test_annotate_total_tags_varying_numbers_of_tags(self, posts):
        queryset = Post.objects.annotate_total_tags()
        for post in queryset:
            assert hasattr(post, 'tags_count')
            assert post.tags_count == post.tags.count()

    def test_annotate_total_tags_no_tags(self):
        post = PostFactory(tags=[])
        queryset = Post.objects.filter(id=post.id).annotate_total_tags()
        assert queryset[0].tags_count == 0

    def test_annotate_total_tags_empty_post_list(self):
        queryset = Post.objects.none().annotate_total_tags()
        assert queryset.count() == 0

    @pytest.mark.skipif(
        'sqlite3' in settings.DATABASES['default']['ENGINE'],
        reason="These tests require PostgreSQL-specific features."
    )
    def test_heavy_search_exact_match(self, posts):
        search_query = posts[0].title.split()[0]  # Search for the first word in the title
        queryset = Post.objects.heavy_search(search_query)
        assert queryset.count() >= 1

    @pytest.mark.skipif(
        'sqlite3' in settings.DATABASES['default']['ENGINE'],
        reason="These tests require PostgreSQL-specific features."
    )
    def test_heavy_search_partial_match(self, posts):
        search_query = posts[0].title[:3]  # Search for a partial match (first 3 chars)
        queryset = Post.objects.heavy_search(search_query)
        assert queryset.count() >= 1

    def test_heavy_search_empty_query(self, posts):
        queryset = Post.objects.heavy_search("")
        assert queryset.count() == 4  # should return all posts or based on other filters

    def test_join_category(self, posts):
        queryset = Post.objects.join_category()
        for post in queryset:
            assert post.category is not None

    def test_join_tags(self, posts):
        queryset = Post.objects.join_tags()
        for post in queryset:
            assert post.tags.count() > 0

    def test_join_category_no_categories(self):
        queryset = Post.objects.none().join_category()
        assert queryset.count() == 0

    def test_join_tags_no_tags(self):
        post = PostFactory(tags=[])
        queryset = Post.objects.filter(id=post.id).join_tags()
        assert queryset[0].tags.count() == 0

    def test_filter_in_date_range_invalid_range(self, posts):
        start_date = timezone.now() + timedelta(days=1)
        end_date = timezone.now() - timedelta(days=1)
        queryset = Post.objects.filter_in_date_range(start_date, end_date)
        assert queryset.count() == 0

    def test_filter_by_category_multiple_matches(self, posts):
        queryset = Post.objects.filter_by_category(category_slug=posts[0].category.slug)
        assert queryset.count() == 2

    def test_filter_by_tag_multiple_matches(self, posts):
        tags = [tag.slug for tag in posts[0].tags.all()]
        queryset = Post.objects.filter_by_tag(tag_slug=tags[0])
        assert queryset.count() == 2

    def test_filter_new_posts_within_specified_days(self, posts):
        queryset = Post.objects.filter_new_posts(days=7)
        for post in queryset:
            assert post.created_at >= timezone.now() - timedelta(days=7)

    def test_annotate_published_since(self, posts):
        queryset = Post.objects.annotate_published_since()
        for post in queryset:
            assert hasattr(post, 'days_since_published')
            assert isinstance(post.days_since_published, timedelta)

    def test_annotate_is_recent_within_7_days(self, posts):
        queryset = Post.objects.annotate_is_recent()
        for post in queryset:
            if post.created_at >= timezone.now() - timedelta(days=7):
                assert post.is_recent is True
            else:
                assert post.is_recent is False

    def test_annotate_next_and_prev(self, posts):
        queryset = Post.objects.annotate_next_and_prev()
        for post in queryset:
            if post.next_post_slug:
                next_post = Post.objects.get(slug=post.next_post_slug)
                assert next_post.pk > post.pk
            if post.prev_post_slug:
                prev_post = Post.objects.get(slug=post.prev_post_slug)
                assert prev_post.pk < post.pk

    @pytest.mark.skipif(
        'sqlite3' in settings.DATABASES['default']['ENGINE'],
        reason="These tests require PostgreSQL-specific features."
    )
    def test_full_text_search_exact_match(self, posts):
        search_query = posts[0].title.split()[0]  # Search for the first word in the title
        queryset = Post.objects.full_text_search(search_query)
        assert queryset.count() >= 1

    @pytest.mark.skipif(
        'sqlite3' in settings.DATABASES['default']['ENGINE'],
        reason="These tests require PostgreSQL-specific features."
    )
    def test_full_text_search_no_match(self):
        search_query = "nonexistentword"
        queryset = Post.objects.full_text_search(search_query)
        assert queryset.count() == 0

    def test_substring_search_partial_match(self, posts):
        search_query = posts[0].title[:3]  # Search for a partial match (first 3 chars)
        queryset = Post.objects.substring_search(search_query)
        assert queryset.count() >= 1

    def test_substring_search_no_match(self):
        search_query = "nonexistentword"
        queryset = Post.objects.substring_search(search_query)
        assert queryset.count() == 0

    @pytest.mark.skipif(
        'sqlite3' in settings.DATABASES['default']['ENGINE'],
        reason="These tests require PostgreSQL-specific features."
    )
    def test_trigram_similarity_search_close_match(self, posts):
        search_query = posts[0].title[:3]  # Search for a trigram match (first 3 chars)
        queryset = Post.objects.trigram_similarity_search(search_query)
        assert queryset.count() >= 1

    @pytest.mark.skipif(
        'sqlite3' in settings.DATABASES['default']['ENGINE'],
        reason="These tests require PostgreSQL-specific features."
    )
    def test_trigram_similarity_search_no_match(self):
        search_query = "nonexistentword"
        queryset = Post.objects.trigram_similarity_search(search_query)
        assert queryset.count() == 0

    @pytest.mark.skipif(
        'sqlite3' in settings.DATABASES['default']['ENGINE'],
        reason="These tests require PostgreSQL-specific features."
    )
    def test_heavy_search_combined_methods(self, posts):
        search_query = posts[0].title.split()[0]  # Search for the first word in the title
        queryset = Post.objects.heavy_search(search_query)
        assert queryset.count() >= 1

    @pytest.mark.skipif(
        'sqlite3' in settings.DATABASES['default']['ENGINE'],
        reason="These tests require PostgreSQL-specific features."
    )
    def test_heavy_search_no_match(self):
        search_query = "nonexistentword"
        queryset = Post.objects.heavy_search(search_query)
        assert queryset.count() == 0

    def test_heavy_search_empty_query(self, posts):
        queryset = Post.objects.heavy_search("")
        assert queryset.count() == 4  # should return all posts or based on other filters

    @pytest.mark.skipif(
        'postgresql' not in settings.DATABASES['default']['ENGINE'],
        reason="This test requires PostgreSQL to execute trigram search."
    )
    def test_heavy_search_fallback_to_substring(self, posts):
        # Full-text search should fail and fall back to substring search
        search_query = "nonexistentword"
        specific_word = posts[0].title[:3]  # A partial match to test fallback
        queryset = Post.objects.heavy_search(specific_word)
        assert queryset.count() >= 1

    @pytest.mark.skipif(
        'postgresql' in settings.DATABASES['default']['ENGINE'],
        reason="This test is for databases other than PostgreSQL."
    )
    def test_trigram_similarity_search_non_postgresql(self):
        search_query = "irrelevant"
        queryset = Post.objects.trigram_similarity_search(search_query)
        assert queryset.count() == 0  # Should return none for non-PostgreSQL databases

    @pytest.mark.skipif(
        'postgresql' in settings.DATABASES['default']['ENGINE'],
        reason="This test is for databases other than PostgreSQL."
    )
    def test_full_text_search_no_query(self, posts):
        queryset = Post.objects.full_text_search("")
        assert queryset.count() == 4
