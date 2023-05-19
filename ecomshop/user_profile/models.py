from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, null=True, blank=True)
