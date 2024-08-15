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

    is_active = models.BooleanField(
        _("Is Active"),
        default=True,
        help_text=_(
            "Indicate whether this tag is currently active and should be displayed "
            "publicly. Deactivate to hide the tag from public view without deleting "
            "it."
        ),
        db_comment="Indicates if the tag is active (true) or hidden from public view (false).",
    )

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

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return f"<Post Tag: {self.title}>"
