from urllib.parse import urlencode

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from sage_tools.mixins.models.base import TimeStampMixin, TitleSlugMixin
from sage_blog.repository.managers import TagDataAccessLayer

class PostTag(TitleSlugMixin, TimeStampMixin):
    """
    Post Tag Model
    """

    objects = TagDataAccessLayer()

    class Meta:
        """
        Meta Information
        """

        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        default_manager_name = "objects"
        db_table = "sage_post_tag"
        db_table_comment = "Table for preserving blog post tags"

    def get_absolute_url(self):
        """
        Get Absolute URL
        """
        base_url = reverse("pages:blog-post-list")
        query_params = urlencode({"tag": self.slug})
        full_url = f"{base_url}?{query_params}"
        return full_url

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return f"<Post Tag: {self.title}>"
