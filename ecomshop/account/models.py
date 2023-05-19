from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
import datetime

# from datetime import datetime

current_date = datetime.date.today()


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            **extra_fields,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save()
        user.is_active = False
        return user

    def create_superuser(self, first_name, last_name, email, username, password, phone_number):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, unique=True)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    signup_day = models.CharField(max_length=50, default=current_date.day)
    signup_month = models.CharField(max_length=50, default=current_date.month)
    signup_year = models.CharField(max_length=50, default=current_date.year)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

# class UserBase(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField('email address', unique=True)
#     name = models.CharField(max_length=255)
#     user_name = models.CharField(max_length=150, unique=True)
#     phone_number = models.CharField(max_length=20, unique=True)
#     image = models.ImageField(upload_to='images/', blank=True)
#     # password1 = models.CharField(max_length=255)
#     # password2 = models.CharField(max_length=255)
#     # Delivery details
#
#     postcode = models.CharField(max_length=12, blank=True)
#     address_line_1 = models.CharField(max_length=150, blank=True)
#     address_line_2 = models.CharField(max_length=150, blank=True)
#     town_city = models.CharField(max_length=150, blank=True)
#     # User Status
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#
#     objects = CustomAccountManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['user_name', 'phone_number']
#
#     class Meta:
#         verbose_name = "Accounts"
#         verbose_name_plural = "Accounts"
#
#     def __str__(self):
#         return self.user_name
# from django.db import models
# from django.utils import timezone
# from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
#
#
# class CustomAccountManager(BaseUserManager):
#
#     def create_superuser(self, email, user_name, first_name, password, **other_fields):
#
#         other_fields.setdefault('is_staff', True)
#         other_fields.setdefault('is_superuser', True)
#         other_fields.setdefault('is_active', True)
#
#         if other_fields.get('is_staff') is not True:
#             raise ValueError(
#                 'Superuser must be assigned to is_staff=True.')
#         if other_fields.get('is_superuser') is not True:
#             raise ValueError(
#                 'Superuser must be assigned to is_superuser=True.')
#
#         return self.create_user(email, user_name, first_name, password, **other_fields)
#
#     def create_user(self, email, user_name, first_name, password, **other_fields):
#
#         if not email:
#             raise ValueError(_('You must provide an email address'))
#
#         email = self.normalize_email(email)
#         user = self.model(email=email, user_name=user_name,
#                           first_name=first_name, **other_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
#
# class NewUser(AbstractBaseUser, PermissionsMixin):
#
#     email = models.EmailField(_('email address'), unique=True)
#     user_name = models.CharField(max_length=150, unique=True)
#     first_name = models.CharField(max_length=150, blank=True)
#     start_date = models.DateTimeField(default=timezone.now)
#     about = models.TextField(_(
#         'about'), max_length=500, blank=True)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=False)
#
#     objects = CustomAccountManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['user_name', 'first_name']
#
#     def __str__(self):
#         return self.user_name
