from django.contrib import admin

# Register your models here.
from apps.user.models import User

admin.site.register(User)
