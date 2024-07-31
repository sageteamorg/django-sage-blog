from django.conf import settings
from django.views.generic.base import ContextMixin


class PaginatedMixin(ContextMixin):
    paginate_by = getattr(settings, "BLOG_POST_PER_PAGE", 15)
