from django.contrib.auth.backends import BaseBackend
from .models import User


# Custom mobile auth backend
class MobileAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        """ Authenticate user with mobile number """
        try:
            user = User.objects.get(mobile=username)
            return user if user.check_password(password) else None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """ Return user by given id """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
