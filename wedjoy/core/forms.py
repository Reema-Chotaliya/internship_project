from django.contrib.auth.forms import UserCreationForm
from .models import User, UserPost
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
    
class UserUpdateProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'firstName',
            'lastName',
            'phone_number',
            'email',
            'gender',
            'address',
            'city',
            'state',
        ]

        widgets = {
            'gender': forms.RadioSelect(),
        }
    
class UserPasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


# ------ user profile comments form ---- 
class UserPostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': "Drop what’s happening around you...",
                'class': 'form-control'
            })
        }