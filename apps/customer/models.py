from django.db import models
from application.custom_models import DateTimeModel
from apps.user.models import User

class Customer(DateTimeModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_user',null=True)
    first_name = models.CharField('Full Name', max_length=30, blank=True)
    phone_number = models.BigIntegerField(blank=True, null=True, unique=True)
    
    def __str__(self):
        return self.user.first_name

    def delete(self, using=None):
        if self.user:
            self.user.delete()
        super(Customer, self).delete(using)
