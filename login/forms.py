from django import forms
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class RegisterUserCompany(forms.Form):
    company_email = forms.EmailField()
    username = forms.CharField(max_length = 20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    repeat_password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    company_name = forms.CharField()
    business_address = forms.CharField(widget=TinyMCE(attrs={'cols': 10, 'rows': 8}), required = False)
    company_registration_number = forms.CharField()
    contract = forms.CharField(label='Select Your Contract', widget=forms.Select(choices=[('2hour', '2 Hours a Month')]))
