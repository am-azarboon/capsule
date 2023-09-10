from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.db import models

from django_jalali.db import models as j_models
from .managers import CustomUserManager


# Custom User model
class User(AbstractUser):
    username = models.EmailField(_("Email Address"), max_length=64, unique=True)
    mobile = models.CharField(_("Mobile number"), max_length=11, unique=True, null=True, blank=True)
    full_name = models.CharField(_("Name"), max_length=64, null=True, blank=True)
    verify = models.BooleanField(_("Is_verify"), default=False)
    melli = models.CharField(_("Melli code"), max_length=10, null=True, blank=True)
    date_of_birth = j_models.jDateField(_("Date of birth"), null=True, blank=True)
    image = models.ImageField(_("Profile image"), null=True, blank=True, upload_to="img/profile")
    first_name = None
    last_name = None
    email = None

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []


# PasswordResetToken model
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="password_reset_tokens")
    token = models.CharField(_("Token"), max_length=64, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=True)
    expired_at = models.DateTimeField(_("Expired at"), default=timezone.now() + timezone.timedelta(hours=4))
    
    def save(self, *args, **kwargs):
        """ Generate new unique random token before saving object """
        if not self.token:
            self.token = get_random_string(length=32)

        while self._meta.model.objects.filter(token=self.token).exists():
            self.token = get_random_string(length=32)

        super().save(*args, **kwargs)
