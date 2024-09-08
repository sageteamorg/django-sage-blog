from django.views.generic.base import ContextMixin

from sage_blog.models import Post, PostCategory, PostTag


class SageBlogContextMixin(ContextMixin):
    categories_context_name = "sage_blog_categories"
    recent_posts_context_name = "sage_blog_recent_posts"
    tags_context_name = "sage_blog_tags"
    recent_posts_limit = 3
    tags_days_ago = 0
    tags_min_count = 1
    tags_limit = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.categories_context_name] = PostCategory.objects.annotate_total_posts()
        context[self.recent_posts_context_name] = Post.objects.filter_recent_posts(
            self.recent_posts_limit
        )
        context[self.tags_context_name] = (
            PostTag.objects.exclude_unpublished_posts()
            .annotate_total_posts()
            .filter_trend_tags(
                days_ago=self.tags_days_ago,
                min_count=self.tags_min_count,
                limit=self.tags_limit,
            )
        )
        return context
