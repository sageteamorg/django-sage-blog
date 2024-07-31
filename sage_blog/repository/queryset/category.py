from django.db.models import Count, Q, QuerySet


class CategoryQuerySet(QuerySet):
    """
    Post Category Querysets
    """

    def annotate_total_posts(self):
        """
        Annotates each category with the total number of posts in that category.

        This method uses Django's Count aggregation function to count the number
        of posts associated with each category. The resulting queryset will have
        an additional attribute 'total_posts' for each category object, which
        indicates the count of posts in that category.
        """
        active_posts_condition = Q(posts__is_active=True)
        qs = self.annotate(total_posts=Count("posts", filter=active_posts_condition))
        return qs
