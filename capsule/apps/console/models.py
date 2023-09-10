from django.utils.translation import gettext as _
from django.db import models

from .enums import DifficultyChoices, UsernameTypesChoices
from .validators import pass_difficulty, account_type
from apps.account.models import User


# Passwords model
class Password(models.Model):
    Difficulty = DifficultyChoices
    UsernameTypes = UsernameTypesChoices

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"), related_name="passwords")
    title = models.CharField(_("Title"), max_length=64, null=True, blank=True)
    address = models.CharField(_("Website address"), max_length=64, null=True, blank=True)
    username = models.CharField(_("Username"), max_length=128)
    password = models.CharField(_("Password"), max_length=128)
    difficulty = models.CharField(_("Difficulty"), max_length=8, choices=Difficulty.choices, default=Difficulty.GOOD)
    type = models.CharField(_("Username type"), max_length=8, choices=UsernameTypes.choices, default=UsernameTypes.EMAIL)
    name = models.CharField(_("Name"), max_length=64, null=True, blank=True)
    melli = models.CharField(_("Melli code"), max_length=10, null=True, blank=True)

    is_archived = models.BooleanField(_("Is archived"), default=False)

    created_at = models.DateTimeField(_("Creation time"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Update time"), auto_now=True)

    class Meta:
        verbose_name = _("Password")
        verbose_name_plural = _("Passwords")

    def save(self, *args, **kwargs):
        self.difficulty = pass_difficulty(self.password)
        self.type = account_type(self.username)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else self.address


# Cards Model
class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"), related_name="cards")
    bank = models.CharField(_("Bank"), max_length=64, null=True, blank=True)
    c_number = models.CharField(_("Card number"), max_length=19)
    cvv2 = models.CharField(_("cvv2"), max_length=4)
    exp_month = models.CharField(_("Expire month"), max_length=2)
    exp_year = models.CharField(_("Expire year"), max_length=2)

    is_archived = models.BooleanField(_("Is archived"), default=False)

    created_at = models.DateTimeField(_("Creation time"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Update time"), auto_now=True)

    class Meta:
        verbose_name = _("Card")
        verbose_name_plural = _("Cards")

    def __str__(self):
        return f"{self.bank} {self.c_number}"
