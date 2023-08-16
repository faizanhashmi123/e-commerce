from django.db import models
from application.custom_models import DateTimeModel
from apps.user.models import User


# Create your models here.
class Merchant(DateTimeModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='merchant_user')
    description = models.TextField()
    phone_number = models.BigIntegerField(blank=True, null=True, unique=True)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.user.email

    def delete(self, using=None):
        if self.user:
            self.user.delete()
        super(Merchant, self).delete(using)
