from typing import Any, Optional

from django.db.models import Manager, QuerySet

from ..queryset import TagQuerySet


class TagDataAccessLayer(Manager):
    """
    Post Data Access Layer
    """

    def get_queryset(self):
        """
        Override the default get_queryset method to return a PostQuerySet instance.

        This method ensures that any query made using this manager will utilize
        the custom methods and properties defined in the PostQuerySet.
        """
        return TagQuerySet(self.model, using=self._db)

    def filter_recent_tags(
        self, days_ago: int = 30, limit: Optional[int] = None, obj: Any = None
    ) -> QuerySet:
        """
        Filter tags that have been used in posts within the specified number of days.
        If 'days_ago' is set to zero, the method returns tags sorted by the 'created_at'
        date of their associated posts. An optional 'limit' parameter can restrict the
        number of tags returned.

        Args:
            days_ago (int): The number of days from the current date to look back.
                            If zero, tags are sorted by 'created_at' date.
            limit (int, optional): The maximum number of tags to return. If None, no
                                    limit is applied.
        """
        return self.get_queryset().filter_recent_tags(days_ago, limit, obj)

    def filter_trend_tags(
        self, days_ago: int = 30, min_count: int = 5, limit: Optional[int] = None
    ) -> QuerySet:
        """
        Filters and retrieves tags based on their usage frequency in posts,
        identifying trending tags either within a specific timeframe or overall.

        This method functions differently based on the `days_ago` parameter:
        - If `days_ago` is zero, it identifies trending tags regardless of the time
        frame, ranking them by their total usage count in posts.
        - If `days_ago` is greater than zero, it filters tags used more than `min_count`
        times in the specified number of days before the current date.

        An optional `limit` parameter allows controlling the maximum number of tags
        returned.

        Args:
            `days_ago` (int): The number of days to look back for identifying trends. If
                            zero, trends are identified based on total usage count.
            `min_count` (int): The minimum number of times a tag must be used to be
                            considered  trending within the specified timeframe.
            `limit` (int, optional): The maximum number of tags to return. If None, no
                                    limit is applied.

        Examples:
            To get overall trending tags with no time restriction:
            >>> trending_tags = Tag.objects.filter_trend_tags(days_ago=0)

            To get tags that are trending in the last 7 days, used at least 10 times:
            >>> weekly_trends = Tag.objects.filter_trend_tags(days_ago=7, min_count=10)

            To get the top 5 overall trending tags:
            >>> top_tags = Tag.objects.filter_trend_tags(days_ago=0, limit=5)

            To get the top 3 trending tags in the last 30 days:
            >>> monthly = Tag.objects.filter_trend_tags(days_ago=30, min_count=5, limit=3)
        """
        return self.get_queryset().filter_trend_tags(days_ago, min_count, limit)

    def annotate_total_posts(self) -> QuerySet:
        """
        Annotate tags with the total number of associated posts.
        """
        return self.get_queryset().annotate_total_posts()

    def search(self, search_term) -> QuerySet:
        """
        Performs a case-insensitive search for tags based on their name.
        """
        return self.get_queryset().search(search_term)

    def filter_by_posts_category(self, category_title) -> QuerySet:
        """
        Filters tags based on the category of associated posts.
        """
        return self.get_queryset().filter_by_posts_category(category_title)

    def exclude_unpublished_posts(self) -> QuerySet:
        """
        Excludes tags that are only associated with inactive or discontinued posts.
        """
        return self.get_queryset().exclude_unpublished_posts()

    def sort_by_popularity(self) -> QuerySet:
        """
        Sorts tags based on the number of posts associated with each, in descending
        order.
        """
        return self.get_queryset().sort_by_popularity()

    def filter_by_post_date_range(self, start_date, end_date) -> QuerySet:
        """
        Filters tags based on the publication date range of the associated posts.
        """
        return self.get_queryset().filter_by_post_date_range(start_date, end_date)

    
    def filter_published(self, is_published=True):
        """
        Filters categories based on their active status.
        """
        return self.get_queryset().filter_published(is_published)

    def filter_published_posts(self, is_published=True):
        """
        Prefetches related posts for each category in the queryset.
        """
        return self.get_queryset().filter_published_posts(is_published)
