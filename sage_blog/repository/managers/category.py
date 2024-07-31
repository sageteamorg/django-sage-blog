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
