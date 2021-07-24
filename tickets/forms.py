from django import forms
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class NewTicketForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=100)
    priority = forms.CharField(label='Priority', widget=forms.Select(choices=[('ST', 'Normal'),('HI', 'High'),('VH', 'Very High'), ('CR', 'Critical')]))
    category = forms.CharField(label='Category', widget=forms.Select(choices=[('normal', 'Normal'),('high', 'High'),('vhigh', 'Very High'), ('critical', 'Critical')]))
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = FlatPage

class CommentForm(forms.Form):
    commenter = forms.CharField(widget=forms.HiddenInput(), required = False)
    comment = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required = False)
    file_upload = forms.FileField(required = False)
