"""
FAQ Administrators
"""

from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin

from sage_blog.models import PostFaq
from sage_blog.resources import PostFaqResource


@admin.register(PostFaq)
class PostFaqAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    """
    FAQ Admin
    """

    resource_class = PostFaqResource

    admin_priority = 5
    list_display = ("question", "post", "created_at", "modified_at")
    list_filter = ("created_at", "modified_at")
    search_fields = ("question", "answer", "post__title")
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
