from django import forms
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE
from hcaptcha.fields import hCaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    hcaptcha = hCaptchaField()

class NewTicketForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=100)
    priority = forms.CharField(label='Priority', widget=forms.Select(choices=[('ST', 'Normal'),('HI', 'High'),('VH', 'Very High'), ('CR', 'Critical')]))
    category = forms.CharField(label='Category', widget=forms.Select(choices=[('normal', 'Normal'),('high', 'High'),('vhigh', 'Very High'), ('critical', 'Critical')]))
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    hcaptcha = hCaptchaField()

    class Meta:
        model = FlatPage

class CommentForm(forms.Form):
    commenter = forms.CharField(widget=forms.HiddenInput(), required = False)
    comment = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required = False)
    hcaptcha = hCaptchaField()

class AccountUpdateForm(forms.Form):
    company_name = forms.CharField()
    address = forms.CharField(widget=TinyMCE(attrs={'cols': 10, 'rows': 8}), required = False)
    company_registration_number = forms.CharField()
    company_email = forms.EmailField()

class CreateNewUser(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())
