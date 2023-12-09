from django import forms
from .models import Accounts,UserProfile


class SingupForm(forms.ModelForm):
    class Meta:
        model=Accounts
        fields=['first_name','last_name','email','password']

class UserprofileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['phone_numper']

#==============

class EditAccountsForm(forms.ModelForm):
    class Meta:
        model=Accounts
        fields=['first_name','last_name']
class EditProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['phone_numper','address_line_1','address_line_2','profile_pictuer','city','state','country']