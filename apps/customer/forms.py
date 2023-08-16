from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Customer
User = get_user_model()

class CreateCustomerUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password2')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'password1']


class CreateCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name','phone_number']

class EditCustomerUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'is_active', 'password']