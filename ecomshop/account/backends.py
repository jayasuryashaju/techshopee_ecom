
from django.contrib.auth.backends import BaseBackend
from .models import User


class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, **kwargs):
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
