from datetime import timedelta

from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchVector, TrigramSimilarity
from django.db.models import (
    BooleanField,
    Case,
    OuterRef,
    Subquery,
    Count,
    ExpressionWrapper,
    F,
    Q,
    QuerySet,
    Value,
    When,
    fields,
)
from django.db.models.functions import Now
from django.utils import timezone


class PostQuerySet(QuerySet):
    """
    A custom QuerySet class for the Post model, providing additional methods for
    querying blog posts.

    This class extends the basic functionality of Django's QuerySet to include methods
    specific to the needs of the blog application, such as filtering posts by various
    criteria and annotating posts with additional computed information.
    """

    def filter_actives(self, is_active=True):
        """
        Returns a queryset of posts filtered by their active status.
        """
        return self.filter(is_active=is_active)

    def filter_recent_posts(self, num_posts=5, obj=None):
        """
        Retrieves a specified number of the most recently created posts.
        If 'obj' is provided, it excludes that object from the results.
        """
        queryset = self.order_by("-created_at")
        
        if obj:
            queryset = queryset.exclude(Q(pk=obj.pk))

        return queryset[:num_posts]

    def filter_by_category(self, category_slug):
        """
        Filters posts by a given category slug.
        """
        return self.filter(category__slug=category_slug)

    def filter_by_tag(self, tag_slug):
        """
        Filters posts by a given tag slug.
        """
        return self.filter(tags__slug=tag_slug)

    def filter_in_date_range(self, start_date, end_date):
        """
        Filters posts created within a specified date range.
        """
        return self.filter(created_at__range=[start_date, end_date])

    def filter_new_posts(self, days=7):
        """
        Fetches posts that are considered 'new', i.e., created within the specified
        number of recent days.
        """
        recent_date = timezone.now() - timedelta(days=days)
        return self.filter(created_at__gte=recent_date)

    def annotate_total_tags(self):
        """
        Annotates each post in the queryset with the count of its associated tags.
        """
        return self.annotate(tags_count=Count("tags"))

    def annotate_published_since(self):
        """
        Annotates each post in the queryset with the number of days since it was
        published.
        """
        return self.annotate(
            days_since_published=ExpressionWrapper(
                Now() - F("created_at"), output_field=fields.DurationField()
            )
        )

    def annotate_is_recent(self):
        """
        Annotates each post in the queryset with a boolean indicating if it is recent
        (created within the last 7 days).
        """
        recent_threshold = timezone.now() - timedelta(days=7)
        return self.annotate(
            is_recent=Case(
                When(created_at__gte=recent_threshold, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        )

    def annotate_next_and_prev(self):
        """
        Annotates each post in the queryset with slugs of the next and previous posts
        in the same category.

        This method uses subqueries to determine the 'slug' of the next and previous posts
        based on their primary key (pk) within the same category. The result is the addition
        of two new fields to each post object in the queryset: `next_post_slug` and
        `prev_post_slug`.

        Usage:
            # Example usage:
            >>> post.dal.annotate_next_and_prev()
        """
        next_post_slug = (
            self.filter(category=OuterRef("category"), pk__gt=OuterRef("pk"))
            .order_by("pk")
            .values("slug")[:1]
        )

        # Get the slug of the previous post
        prev_post_slug = (
            self.filter(category=OuterRef("category"), pk__lt=OuterRef("pk"))
            .order_by("-pk")
            .values("slug")[:1]
        )

        # Annotate the current queryset with the slugs
        return self.annotate(
            next_post_slug=Subquery(next_post_slug),
            prev_post_slug=Subquery(prev_post_slug),
        )

    def full_text_search(self, search_query):
        """
        Performs a full-text search on 'title' and 'description' fields of the posts.
        This method is optimized for finding complete words or phrases, not partial
        substrings.
        """
        if search_query:
            vector = SearchVector("title", "description")
            query = SearchQuery(search_query)
            return self.annotate(search=vector).filter(search=query)
        return self

    def substring_search(self, search_query):
        """
        Performs a case-insensitive substring search in 'title' and 'description'
        fields of the posts. This method is useful for partial word matching, but it is
        less efficient than full-text search.
        """
        if search_query:
            return self.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
            )
        return self

    def trigram_similarity_search(self, search_query):
        """
        Performs a search using trigram similarity on 'title' and 'description' fields
        of the posts.
        This method supports partial word matches and is more linguistically aware than
        a simple substring search, but it requires PostgreSQL with pg_trgm extension.
        """
        if search_query and "postgresql" in settings.DATABASES["default"]["ENGINE"]:
            return (
                self.annotate(
                    similarity=TrigramSimilarity("title", search_query)
                    + TrigramSimilarity("description", search_query)
                )
                .filter(similarity__gt=0.1)
                .order_by("-similarity")
            )
        return self.none()

    def heavy_search(self, search_query):
        """
        Combines full-text search, substring search, and trigram similarity search to
        provide a comprehensive search experience. The method first tries a full-text
        search. If it yields no results, it falls back to a substring search. If
        available and suitable, it also uses trigram similarity for nuanced matching.
        """
        if not search_query:
            return self

        # Step 1: Full-text search
        full_text_qs = self.full_text_search(search_query)
        if full_text_qs.exists():
            return full_text_qs

        # Step 2: Substring search
        substring_qs = self.substring_search(search_query)
        if substring_qs.exists():
            return substring_qs

        # Step 3: Trigram similarity search (if supported by the database)
        if "postgresql" in settings.DATABASES["default"]["ENGINE"]:
            trigram_qs = self.trigram_similarity_search(search_query)
            if trigram_qs.exists():
                return trigram_qs

        return self.none()

    def join_category(self):
        """
        Join Category Table
        """
        return self.select_related("category")

    def join_tags(self):
        """
        Join Tag Table
        """
        return self.prefetch_related("tags")
