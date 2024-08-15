from urllib.parse import urlencode

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from sage_tools.mixins.models.base import TimeStampMixin, TitleSlugMixin
from sage_blog.repository.managers import CategoryDataAccessLayer


class PostCategory(TitleSlugMixin, TimeStampMixin):
    """
    Post Category
    """

    is_active = models.BooleanField(
        _("Is Active"),
        default=True,
        help_text=_(
            "Indicate whether this category is currently active and should be displayed "
            "publicly. Deactivate to hide the category from public view without deleting "
            "it."
        ),
        db_comment="Indicates if the category is active (true) or hidden from public view (false).",
    )

    objects = CategoryDataAccessLayer()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        default_manager_name = "objects"
        db_table = "sage_post_category"
        db_table_comment = "Table for categorizing blog posts"

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return f"<Post Category: {self.title}>"
