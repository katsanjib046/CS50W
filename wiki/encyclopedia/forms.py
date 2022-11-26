from logging import PlaceHolder
from django import forms


class createForm(forms.Form):
    title = forms.CharField(max_length=100, label="Title", required=True)
    body = forms.CharField(widget=forms.Textarea, label="Body", required=True)