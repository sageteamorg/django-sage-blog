from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

try:
    from sorl.thumbnail.fields import ImageField
except ImportError:
    raise ImportError(  # noqa: B904
        "Install `sorl-thumbnail` package. Run `pip install sorl-thumbnail`."
    )

try:
    import readtime
except ImportError:
    raise ImportError(
        "Install `readtime` package. Run `pip install readtime` "
    )

from sage_seo.models.mixins.seo import SEOMixin, BlogDetailJsonLdMixin
from sage_tools.mixins.models.abstract import PictureOperationAbstract
from sage_tools.mixins.models.base import (
    TimeStampMixin,
    TitleSlugDescriptionMixin
)


class Post(
    TitleSlugDescriptionMixin,
    PictureOperationAbstract,
    SEOMixin,
    BlogDetailJsonLdMixin,
    TimeStampMixin):
    """
    Represents a blog post in the system.
    """

    is_active = models.BooleanField(
        _("Is Active"),
        default=True,
        help_text=_(
            "Indicate whether this post is currently active and should be displayed "
            "publicly. Deactivate to hide the post from public view without deleting "
            "it."
        ),
        db_comment="Indicates if the post is active (true) or hidden from public view (false).",
    )

    summary = models.CharField(
        _("Summary"),
        max_length=140,
        null=True,
        blank=False,
        help_text=_("Enter a brief summary of the post, up to 140 characters."),
        db_comment="A brief summary of the blog post.",
    )

    picture = ImageField(
        _("Picture of Post"),
        upload_to="blog/posts/",
        width_field="width_field",
        height_field="height_field",
        help_text=_(
            "Upload an image representing the post. Ideal dimensions are [x] by [y]."
        ),
        db_comment="Image file associated with the blog post.",
    )

    banner = ImageField(
        _("Banner of Post Detail"),
        upload_to="blog/posts/",
        null=True,
        blank=True,
        help_text=_(
            "Upload an image representing the post. Ideal dimensions are [x] by [y]."
        ),
        db_comment="Image file associated with the blog post.",
    )

    published_at = models.DateTimeField(
        _("Published At"),
        default=timezone.now,
        help_text=_("The date and time when the post was published.")
    )

    tags = models.ManyToManyField(
        "PostTag",
        related_name="posts",
        verbose_name=_("Tags"),
        help_text=_("Select or add tags to categorize the post."),
    )

    category = models.ForeignKey(
        "PostCategory",
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("Category"),
        help_text=_("Choose the category of the post."),
        db_comment="The category to which the blog post belongs.",
    )

    objects = models.Manager()

    def get_absolute_url(self):
        """
        Returns the absolute URL for the blog post detail page.

        This method is used to provide a direct link to the blog post's detail view.
        """
        return reverse("pages:blog-post-detail", kwargs={"post_slug": self.slug})

    class Meta:
        """
        Meta options for the Post model.

        Provides metadata and configurations for the Post model such as verbose names
        and other options specific to this model.
        """

        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        default_manager_name = "objects"
        db_table = 'sage_post'
        db_table_comment = 'Table for preserving blog posts'

    @property
    def reading_time(self):
        """
        Estimate the reading time of the description using the `readtime` library.

        Returns:
            int: Estimated reading time in minutes.
        """
        result = readtime.of_text(self.description)
        # Extracting minutes from the result text (e.g., "1 min read" -> 1)
        minutes = int(result.text.split()[0])  # assuming the format is always "X min read"
        return minutes


    def __str__(self):
        return str(self.title)

    def __repr__(self):
        """
        Developer-friendly string representation of the Post instance.

        Returns the title of the post, which helps in identifying the instance when
        printed or logged, especially during debugging.
        """
        return f"<Post: {self.title}>"
