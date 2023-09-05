from django.utils.translation import gettext as _
from django.contrib.auth.models import BaseUserManager


# Custom UserManager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, full_name=None):
        """Create and save a User with the given username(email) and password. """
        if not username:
            raise ValueError(_("Users must have an email address"))

        user = self.model(username=self.normalize_email(username), full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """Create and save a superuser with the given username(email) and password. """
        user = self.create_user(username, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.verify = True
        user.save(using=self._db)
        return user
