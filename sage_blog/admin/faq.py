"""
FAQ Administrators
"""
from django.contrib import admin

from sage_blog.models import PostFaq


@admin.register(PostFaq)
class PostFaqAdmin(admin.ModelAdmin):
    """
    FAQ Admin
    """

    admin_priority = 5
    list_display = (
        "question",
        "post",
        "created_at",
        "modified_at"
    )
    list_filter = (
        "created_at",
        "modified_at"
    )
    search_fields = (
        "question",
        "answer",
        "post__title"
    )
    list_select_related = ("post",)
    autocomplete_fields = ("post",)
    fieldsets = (
        (None, {"fields": ("question", "answer", "post")}),
        (
            "Timestamps",
            {"fields": ("created_at", "modified_at"), "classes": ("collapse",)},
        ),
    )
    readonly_fields = ("created_at", "modified_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
