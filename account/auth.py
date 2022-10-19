from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import User


class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(email=username))
            return user
        except:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(Q(id=user_id))
            return user
        except:
            return None
