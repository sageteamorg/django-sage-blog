from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from sage_blog.models import PostTag


@admin.register(PostTag)
class PostTagAdmin(admin.ModelAdmin):
    """
    Django admin customization for the PostTag model.

    This admin class customizes the display and search capabilities for PostTags
    in the Django admin interface. It provides an easy-to-use interface for managing
    tags associated with blog posts.
    """

    admin_priority = 3
    list_display = ("title", "slug", "is_published", "modified_at")
    list_filter = ("created_at", "modified_at")
    search_fields = ("title",)
    date_hierarchy = "created_at"
    save_on_top = True
    ordering = ("title",)

    fieldsets = (
        (None, {"fields": ("title", "slug", "is_published")}),
        (_("Timestamps"), {"fields": ("created_at", "modified_at")}),
    )
    readonly_fields = ("created_at", "modified_at", "slug")
