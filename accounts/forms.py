from django import forms
from .models import Accounts


class SingupForm(forms.ModelForm):
    class Meta:
        model=Accounts
        fields=['first_name','last_name','phone_numper','email','username','profile_pictuer','password']
