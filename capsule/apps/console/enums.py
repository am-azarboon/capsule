from django.utils.translation import gettext as _
from django.db.models import TextChoices


# Passwords difficulty choices
class DifficultyChoices(TextChoices):
    HARD = "h", _("Hard")
    GOOD = "g", _("Good")
    WEAK = "w", _("Weak")


# UsernameTypes choices
class UsernameTypesChoices(TextChoices):
    EMAIL = "e", _("Email")
    PHONE = "p", _("Phone")
