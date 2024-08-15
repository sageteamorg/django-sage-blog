from django.db.models import Manager

from ..queryset import CategoryQuerySet


class CategoryDataAccessLayer(Manager):
    """
    Post Data Access Layer
    """

    def get_queryset(self):
        """
        Override the default get_queryset method to return a PostQuerySet instance.

        This method ensures that any query made using this manager will utilize
        the custom methods and properties defined in the PostQuerySet.
        """
        return CategoryQuerySet(self.model, using=self._db)

    def annotate_total_posts(self):
        """
        Annotates each category with the total number of posts in that category.

        This method uses Django's Count aggregation function to count the number
        of posts associated with each category. The resulting queryset will have
        an additional attribute 'total_posts' for each category object, which
        indicates the count of posts in that category.
        """
        return self.get_queryset().annotate_total_posts()

    def get_actives(self, is_active=True):
        """
        Filters categories based on their active status.
        """
        return self.get_queryset().get_actives(is_active)

    def filter_active_posts(self, is_active=True):
        """
        Prefetches related posts for each category in the queryset.
        """
        return self.get_queryset().filter_active_posts(is_active)

    def join_posts(self):
        """
        Excludes categories that are only associated with inactive or discontinued posts.
        """
        return self.get_queryset().join_posts()

    def exclude_inactive_posts(self) -> "QuerySet":
        """
        Excludes categories that are only associated with inactive or discontinued posts.
        """
        return self.get_queryset().exclude_inactive_posts()

    def filter_recent_categories(self, num_categories=5, obj=None):
        """
        Retrieves a specified number of the most recently created categories.
        If 'obj' is provided, it excludes that object from the results.
        """
        return self.get_queryset().filter_recent_categories(num_categories, obj)
