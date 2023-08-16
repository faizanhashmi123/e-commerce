from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from application.custom_models import DateTimeModel
from apps.user.manager import CustomUserManager
from apps.user.constants import USER_TYPE_CHOICES


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    first_name = models.CharField('First name', max_length=30, blank=True)
    last_name = models.CharField('Last name', max_length=150, blank=True)
    username = models.EmailField(
        'username', unique=True, help_text='Username.', null=True
    )
    email = models.EmailField(
        'Email address', unique=True, help_text='Email address.', null=True
    )
    type = models.CharField(choices=USER_TYPE_CHOICES, max_length=20, null=True)
    is_admin = models.BooleanField(default=False, null=True, blank=True)
    phone_number = models.BigIntegerField(blank=True, null=True)
    objects = CustomUserManager()

    class Meta:
        ordering = ('-date_joined',)

    def __str__(self):
        return self.email if self.email else str(self.id)


class Profile(DateTimeModel):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        if self.user:
            return self.user.first_name + ' ' + self.user.last_name if self.user.first_name and self.user.last_name  else self.user.email
        else:
            return str(self.id)

