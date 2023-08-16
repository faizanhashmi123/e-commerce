from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Merchant, User

class CreateMerchantForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = ['phone_number']

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password2')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'email', 'password1']


class EditMerchantUserForm(UserChangeForm):
    type = forms.CharField(widget=forms.HiddenInput(), initial='merchant')
    class Meta:
        model = User
        fields = ['email', 'type', 'is_active', 'password']



class EditMerchantForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = ['phone_number']