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
        published_posts = self.filter_published_posts()
        qs = published_posts.annotate(
            total_posts=Count("posts")
        )
        return qs

    def filter_published(self, is_published: bool = True):
        """
        Filters categories based on their published status.
        """
        qs = self.filter(is_published=is_published)
        return qs

    def filter_published_posts(self, is_published: bool=True):
        """
        Prefetches related posts for each category in the queryset.
        """
        published_posts_condition = Q(
            posts__is_published=is_published
        )
        published = self.filter_published()
        qs = published.filter(published_posts_condition)
        return qs

    def join_posts(self):
        """
        Excludes categories that are only associated with
        in published or discontinued posts.
        """
        qs = self.prefetch_related("posts")
        return qs

    def exclude_unpublished_posts(self) -> QuerySet:
        """
        Excludes categories that are only associated with
        in published or discontinued posts.
        """
        qs = self.filter(
            posts__is_published=True
        )
        return qs

    def filter_recent_categories(self, num_categories=5, obj=None):
        """
        Retrieves a specified number of the most recently created categories.
        If 'obj' is provided, it excludes that object from the results.
        
        Args:
            num_categories (int): The number of recent categories to retrieve.
            obj (Optional[Category]): An optional Category object to exclude
            from the results.

        Returns:
            QuerySet: A queryset of the most recent categories.
        """
        queryset = self.order_by("-created_at")

        if obj:
            queryset = queryset.exclude(Q(pk=obj.pk))

        return queryset[:num_categories]
