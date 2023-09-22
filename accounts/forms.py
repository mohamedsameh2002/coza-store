from django import forms
from .models import Accounts,UserProfile


class SingupForm(forms.ModelForm):
    class Meta:
        model=Accounts
        fields=['first_name','last_name','email','username','password']

class UserprofileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['phone_numper']