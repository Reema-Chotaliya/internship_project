from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['firstName',
            'lastName',
            'email',
            'role',
            'gender',
            'phone_number',
            'address',
            'city',
            'state']
        widgets={
            'password1':forms.PasswordInput(),
            'password2':forms.PasswordInput(),
            'gender': forms.RadioSelect(attrs={'class': 'd-flex'}),
        }
class  UserLoginForm(forms.Form):
    email = forms.EmailField()
    password= forms.CharField(widget=forms.PasswordInput())