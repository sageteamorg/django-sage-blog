from django.conf import settings
from django.db.models import QuerySet
from django.views.generic.base import ContextMixin

from sage_blog.filters import PostFilter


class SearchableMixin(ContextMixin):
    search_param_name = "search"

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        search_query = self.request.GET.get(self.search_param_name, "")

        qs = qs.heavy_search(search_query)

        if not search_query:
            filter_qs = PostFilter(self.request.GET, queryset=qs)
            qs = filter_qs.qs

        return qs
