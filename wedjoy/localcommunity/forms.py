from django import forms
from core.models import User

class OwnerProfileUpdateForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput(),required=False)
    new_password = forms.CharField(widget=forms.PasswordInput(),required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(),required=False)
    
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
    
class EventProfileUpdateForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput(),required=False)
    new_password = forms.CharField(widget=forms.PasswordInput(),required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(),required=False)
    
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
    
