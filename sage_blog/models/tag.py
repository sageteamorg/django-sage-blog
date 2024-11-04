from django.db import models
from django.utils.translation import gettext_lazy as _
from sage_tools.mixins.models.base import TimeStampMixin, TitleSlugMixin

from sage_blog.repository.managers import TagDataAccessLayer


class PostTag(TitleSlugMixin, TimeStampMixin):
    """
    Post Tag Model
    """

    is_published = models.BooleanField(
        _("Is Published"),
        default=True,
        help_text=_(
            "Indicate whether this tag is currently published and should be "
            "displayed to all users. If unpublished, only staff users can view "
            "the tag."
        ),
        db_comment=(
            "Indicates if the tag is published (true) or hidden from non-staff "
            "users (false)."
        ),
    )

    objects: TagDataAccessLayer = TagDataAccessLayer()

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
