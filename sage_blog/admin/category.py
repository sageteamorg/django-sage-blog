from django.contrib import admin
from django.db.models import Count, Q, QuerySet
from django.utils.translation import gettext_lazy as _

from sage_blog.models import PostCategory
from sage_blog.admin.filters import PostsStatusFilter


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    """
    Django admin customization for the PostCategory model.

    This admin class customizes the display and search capabilities for PostCategories
    in the Django admin interface. It provides an intuitive interface for managing blog
    post categories.
    """

    # Display settings
    admin_priority = 1
    list_display = ("title", "slug", "is_active", "modified_at")
    list_filter = (PostsStatusFilter, "is_active")
    search_fields = ("title",)
    date_hierarchy = "created_at"
    ordering = ("title",)
    save_on_top = True

    # Form layout customization
    fieldsets = (
        (None, {"fields": ("title", "slug", "is_active")}),
        (_("Timestamps"), {"fields": ("created_at", "modified_at")}),
    )
    readonly_fields = ("created_at", "modified_at", "slug")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.join_posts()
        # queryset = queryset.prefetch_related("posts")
        return queryset
