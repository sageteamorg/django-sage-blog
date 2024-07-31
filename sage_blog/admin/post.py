from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from sorl.thumbnail.admin import AdminImageMixin

from sage_blog.models import Post, PostFaq


class PostFaqInline(admin.TabularInline):
    model = PostFaq
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin, AdminImageMixin):
    """
    Django admin customization for the Post model.

    This admin class customizes the display, search, and filter capabilities for Posts
    in the Django admin interface. It also provides a customized form layout for
    editing and adding new Posts.
    """

    admin_priority = 2
    inlines = PostFaqInline,
    # Display settings
    list_display = (
        "title",
        "is_active",
        "category",
        "get_tags",
        "get_summary",
        "published_at",
        "modified_at",
    )
    list_filter = (
        "is_active",
        "category",
        "tags",
        "published_at",
        "modified_at"
    )
    search_fields = (
        "title",
        "slug",
        "description",
        "summary",
        "category__title",
        "tags__title"
    )
    filter_horizontal = (
        "tags",
    )
    save_on_top = True
    autocomplete_fields = (
        "category",
    )
    date_hierarchy = "published_at"
    ordering = (
        "-published_at",
    )
    readonly_fields = (
        "created_at",
        "modified_at",
        "slug"
    )
    fieldsets = (
        ("Basic Information", {"fields": ("title", "slug", "category", "is_active")}),
        ("Content Details", {"fields": ("summary", "description", "picture", "banner", "alternate_text")}),
        ("SEO Metadata", {
            "fields": (
                "keywords",
                "meta_description",
                "json_ld",
            ),
            "classes": ("collapse",),
        }),
        ("Open Graph Metadata", {
            "fields": (
                "og_title",
                "og_type",
                "og_image",
                "og_description",
                "og_url",
                "og_site_name",
                "og_locale",
                "article_author",
            ),
            "classes": ("collapse",),
        }),
        ("Tags", {
            "fields": ("tags",),
            "classes": ("collapse",),
        }),
        ("Timestamps", {
            "fields": (
                "published_at",
                "modified_at",
                "created_at",
            ),
            "classes": ("collapse",),
        }),
    )


    def get_tags(self, obj):
        return ", ".join([tag.title for tag in obj.tags.all()])

    get_tags.short_description = _("Tags")

    def get_summary(self, obj):
        return obj.summary if obj.summary else _("No Summary")

    get_summary.short_description = _("Summary")

    # Filter customization
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related("tags")
        return queryset
