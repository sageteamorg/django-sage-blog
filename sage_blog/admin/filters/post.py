from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class PostsStatusFilter(admin.SimpleListFilter):
    title = _("Posts Status")
    parameter_name = "posts_status"

    def lookups(self, request, model_admin):
        return [
            ("no_posts", _("No Posts")),
            ("inactive_posts", _("Only Inactive Posts")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "no_posts":
            return queryset.filter(posts__isnull=True)
        elif self.value() == "inactive_posts":
            return queryset.filter_active_posts().distinct()
        return queryset
