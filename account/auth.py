from django.contrib.auth.backends import BaseBackend
from django.db.models import Q

from .models import User


class AuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(Q(email=username))
            if user.check_password(password):
                return user
        except:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(Q(id=user_id))
            return user
        except:
            return None
