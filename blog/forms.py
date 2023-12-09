from django import forms
from .models import Comments,Reply


class CommentsForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=['comment']

class ReplyForm(forms.ModelForm):
    class Meta:
        model=Reply
        fields=['reply']
