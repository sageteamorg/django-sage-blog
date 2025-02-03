from django.db import models
from django.conf import settings
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

try:
    from sorl.thumbnail.fields import ImageField
except ImportError:
    raise ImportError(  # noqa: B904
        "Install `sorl-thumbnail` package. Run `pip install sorl-thumbnail`."
    )

try:
    import readtime
except ImportError:
    raise ImportError("Install `readtime` package. Run `pip install readtime` ")

from sage_seo.models.mixins.seo import BlogDetailJsonLdMixin, SEOMixin
from sage_tools.mixins.models.abstract import PictureOperationAbstract
from sage_tools.mixins.models.base import TimeStampMixin, TitleSlugDescriptionMixin

from sage_blog.repository.managers import PostDataAccessLayer


class Post(
    TitleSlugDescriptionMixin,
    PictureOperationAbstract,
    SEOMixin,
    BlogDetailJsonLdMixin,
    TimeStampMixin,
):
    """
    Represents a blog post in the system.
    """

    description = CKEditor5Field(
        _("Description"),
        help_text=_(
            "Enter a detailed description of the item. This can include its purpose, "
            "characteristics, and any other relevant information."
        ),
        db_comment="Stores a detailed description of the instance.",
    )

    is_published = models.BooleanField(
        _("Is Published"),
        default=True,
        help_text=_(
            "Indicate whether this post is currently published and should be displayed "
            "to all users. If unpublished, only staff users can view the post."
        ),
        db_comment="Indicates if the post is published (true) or hidden from non-staff users (false).",
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
        upload_to="blog/posts/pictures/",
        width_field="width_field",
        height_field="height_field",
        help_text=_(
            "Upload an image representing the post. Ideal dimensions are [x] by [y]."
        ),
        db_comment="Image file associated with the blog post.",
    )

    banner = ImageField(
        _("Banner of Post Detail"),
        upload_to="blog/posts/banners/",
        null=True,
        blank=True,
        help_text=_(
            "Upload an image representing the post. Ideal dimensions are [x] by [y]."
        ),
        db_comment="Image file associated with the blog post.",
    )

    video = models.FileField(
        _("Video"),
        max_length=110,
        upload_to="blog/posts/videos/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["mp4", "webm", "ogv"]
            )
        ]
    )

    published_at = models.DateTimeField(
        _("Published At"),
        default=timezone.now,
        help_text=_("The date and time when the post was published."),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Author"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        help_text=_("Select the author of the post."),
        db_comment="References the user who authored the post. Can be null if no specific author is assigned.",
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

    suggested_posts = models.ManyToManyField(
        "self",
        verbose_name=_("Suggested posts"),
        blank=True,
        help_text=_("Select other posts to suggest alongside this product."),
    )

    related_posts = models.ManyToManyField(
        "self",
        verbose_name=_("Related posts"),
        blank=True,
        symmetrical=False,
        help_text=_("Select posts related to this product."),
    )

    objects: PostDataAccessLayer = PostDataAccessLayer()

    class Meta:
        """
        Meta options for the Post model.

        Provides metadata and configurations for the Post model such as verbose names
        and other options specific to this model.
        """

        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        default_manager_name = "objects"
        db_table = "sage_post"
        db_table_comment = "Table for preserving blog posts"

    @property
    def reading_time(self):
        """
        Estimate the reading time of the description using the `readtime` library.

        Returns:
            int: Estimated reading time in minutes.
        """
        result = readtime.of_text(self.description)
        # Extracting minutes from the result text (e.g., "1 min read" -> 1)
        minutes = int(
            result.text.split()[0]
        )  # assuming the format is always "X min read"
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
