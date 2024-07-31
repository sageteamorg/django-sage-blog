from urllib.parse import urlencode

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from sage_tools.mixins.models.base import TimeStampMixin, TitleSlugMixin


class PostCategory(TitleSlugMixin, TimeStampMixin):
    """
    Post Category
    """

    objects = models.Manager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        default_manager_name = "objects"
        db_table = 'sage_post_category'
        db_table_comment = 'Table for categorizing blog posts'

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return f"<Post Category: {self.title}>"
