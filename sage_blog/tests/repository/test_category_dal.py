import pytest
from datetime import timedelta
from django.utils import timezone

from ..factories import PostCategoryFactory, PostFactory
from sage_blog.models import PostCategory


@pytest.mark.django_db
class TestCategoryQuerySet:

    @pytest.fixture
    def categories(self):
        # Setup categories, some published and some not
        return [
            PostCategoryFactory(is_published=True),
            PostCategoryFactory(is_published=False),
            PostCategoryFactory(is_published=True),
        ]

    @pytest.fixture
    def categories_with_posts(self):
        # Setup categories with posts
        category1 = PostCategoryFactory(is_published=True)
        category2 = PostCategoryFactory(is_published=True)
        category3 = PostCategoryFactory(is_published=False)

        PostFactory.create_batch(5, category=category1, is_published=True)
        PostFactory.create_batch(3, category=category2, is_published=False)
        PostFactory.create_batch(0, category=category3)

        return [category1, category2, category3]

    def test_filter_published_categories(self, categories):
        queryset = PostCategory.objects.filter_published(is_published=True)
        assert queryset.count() == 2
        for category in queryset:
            assert category.is_published is True

    def test_filter_unpublished_categories(self, categories):
        queryset = PostCategory.objects.filter_published(is_published=False)
        assert queryset.count() == 1
        for category in queryset:
            assert category.is_published is False

    def test_filter_no_published_categories(self):
        # Creating all categories as unpublished
        PostCategory.objects.all().delete()
        PostCategoryFactory.create_batch(3, is_published=False)

        queryset = PostCategory.objects.filter_published(is_published=True)
        assert queryset.count() == 0

    def test_filter_published_posts_categories(self, categories_with_posts):
        queryset = PostCategory.objects.filter_published_posts(is_published=True)
        assert queryset.count() == 5
        for category in queryset:
            assert category.posts.filter(is_published=True).exists()

    def test_filter_unpublished_posts_categories(self, categories_with_posts):
        queryset = PostCategory.objects.filter_published_posts(is_published=False)
        assert queryset.count() == 3
        for category in queryset:
            assert category.posts.filter(is_published=False).exists()


    @pytest.mark.skip(reason="Performance test for large datasets, manually run if needed.")
    def test_filter_published_posts_large_dataset(self):
        # Creating a large dataset for performance testing
        categories = PostCategoryFactory.create_batch(100)
        for category in categories:
            PostFactory.create_batch(100, category=category, is_published=True)
        
        queryset = PostCategory.objects.filter_published_posts(is_published=True)
        assert queryset.count() == 100

    def test_annotate_total_posts_varying(self, categories_with_posts):
        queryset = PostCategory.objects.annotate_total_posts()
        for category in queryset:
            expected_count = category.posts.filter(is_published=True).count()
            assert hasattr(category, 'total_posts')
            assert category.total_posts == expected_count

    def test_annotate_total_posts_no_posts(self):
        empty_category = PostCategoryFactory()
        queryset = PostCategory.objects.filter(id=empty_category.id).annotate_total_posts()
        assert queryset.count() == 0

    def test_annotate_total_posts_empty_category_list(self):
        queryset = PostCategory.objects.none().annotate_total_posts()
        assert queryset.count() == 0

    def test_filter_recent_categories_various_values(self):
        # Creating categories with different creation times
        PostCategoryFactory(created_at=timezone.now() - timedelta(days=10))
        PostCategoryFactory(created_at=timezone.now() - timedelta(days=5))
        PostCategoryFactory(created_at=timezone.now() - timedelta(days=1))

        queryset = PostCategory.objects.filter_recent_categories(num_categories=2)
        assert queryset.count() == 2
        assert queryset[0].created_at >= queryset[1].created_at  # Ensure they're ordered by recency

    def test_filter_recent_categories_excluding_specific_category(self):
        recent_category = PostCategoryFactory(created_at=timezone.now() - timedelta(days=1))
        old_category = PostCategoryFactory(created_at=timezone.now() - timedelta(days=30))

        queryset = PostCategory.objects.filter_recent_categories(num_categories=1, obj=recent_category)
        assert queryset.count() == 1
        assert old_category in queryset
