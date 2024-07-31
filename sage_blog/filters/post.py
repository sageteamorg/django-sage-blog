from typing import ClassVar

import django_filters

from sage_blog.models import Post


class PostFilter(django_filters.FilterSet):
    """
    A custom filter set for the Post model in a Django application.

    This filter set is designed to filter blog posts based on categories and tags. It
    uses django-filters, an extension to Django for creating dynamic query filters.
    `PostFilter` facilitates filtering the list of blog posts on the basis of category
    and tag slugs.
    """

    cat = django_filters.CharFilter(field_name="category", lookup_expr="slug")
    tag = django_filters.CharFilter(field_name="tags", lookup_expr="slug")

    class Meta:
        """
        Meta
        """

        model = Post
        fields: ClassVar = ["cat", "tag"]
