from django.db.models import Count, Manager

from ..queryset.post import PostQuerySet


class PostDataAccessLayer(Manager):
    """
    Post Data Access Layer
    """

    def get_queryset(self):
        """
        Override the default get_queryset method to return a PostQuerySet instance.

        This method ensures that any query made using this manager will utilize
        the custom methods and properties defined in the PostQuerySet.
        """
        return PostQuerySet(self.model, using=self._db)

    def filter_actives(self, is_published=True):
        """
        Returns a queryset of posts filtered by their active status.
        """
        return self.get_queryset().filter_actives(is_published)

    def filter_recent_posts(self, num_posts=5):
        """
        Retrieves a specified number of the most recently created posts.
        If 'obj' is provided, it excludes that object from the results.
        """
        return self.get_queryset().filter_recent_posts(num_posts=num_posts)

    def filter_by_category(self, category_slug):
        """
        Filters posts by a given category slug.
        """
        return self.get_queryset().filter_by_category(category_slug=category_slug)

    def filter_by_tag(self, tag_slug):
        """
        Filters posts by a given tag slug.
        """
        return self.get_queryset().filter_by_tag(tag_slug=tag_slug)

    def filter_in_date_range(self, start_date, end_date):
        """
        Filters posts created within a specified date range.
        """
        return self.get_queryset().filter_in_date_range(start_date, end_date)

    def filter_new_posts(self, days=7):
        """
        Fetches posts that are considered 'new', i.e., created within the specified
        number of recent days.
        """
        return self.get_queryset().filter_new_posts(days)

    def annotate_total_tags(self):
        """
        Annotates each post in the queryset with the count of its associated tags.
        """
        return self.get_queryset().annotate_total_tags()

    def annotate_published_since(self):
        """
        Annotates each post in the queryset with the number of days since it was
        published.
        """
        return self.get_queryset().annotate_published_since()

    def annotate_is_recent(self):
        """
        Annotates each post in the queryset with a boolean indicating if it is recent
        (created within the last 7 days).
        """
        return self.get_queryset().annotate_is_recent()

    def full_text_search(self, search_query):
        """
        Performs a full-text search on 'title' and 'description' fields of the posts.
        This method is optimized for finding complete words or phrases, not partial
        substrings.
        """
        return self.get_queryset().full_text_search(search_query)

    def substring_search(self, search_query):
        """
        Performs a case-insensitive substring search in 'title' and 'description'
        fields of the posts. This method is useful for partial word matching, but it is
        less efficient than full-text search.
        """
        return self.get_queryset().substring_search(search_query)

    def trigram_similarity_search(self, search_query):
        """
        Performs a search using trigram similarity on 'title' and 'description' fields
        of the posts.
        This method supports partial word matches and is more linguistically aware than
        a simple substring search, but it requires PostgreSQL with pg_trgm extension.
        """
        return self.get_queryset().trigram_similarity_search(search_query)

    def heavy_search(self, search_query):
        """
        Combines full-text search, substring search, and trigram similarity search to
        provide a comprehensive search experience. The method first tries a full-text
        search. If it yields no results, it falls back to a substring search. If
        available and suitable, it also uses trigram similarity for nuanced matching.
        """
        return self.get_queryset().heavy_search(search_query)

    def join_category(self):
        return self.get_queryset().join_category()

    def join_tags(self):
        return self.get_queryset().join_tags()
