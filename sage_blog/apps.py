from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class SageBlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sage_blog"
    verbose_name = _("Blog")
