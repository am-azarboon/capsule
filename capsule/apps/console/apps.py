from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class ConsoleConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.console"
    verbose_name = _("Console")
