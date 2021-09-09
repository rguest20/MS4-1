from django import forms
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE
from hcaptcha.fields import hCaptchaField
from django.core.validators import *


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username', max_length=100, validators=[
            MinLengthValidator(
                1, message="This field cannot be empty")])
    password = forms.CharField(
        widget=forms.PasswordInput(), validators=[
            MinLengthValidator(
                1, message="This field cannot be empty")])


class NewTicketForm(forms.Form):
    subject = forms.CharField(
        label='Subject', max_length=100, validators=[
            MinLengthValidator(
                1, message="This field cannot be empty")])
    priority = forms.CharField(
        label='Priority', widget=forms.Select(
            choices=[
                ('ST', 'Normal'), ('HI', 'High'), ('VH', 'Very High'), ('CR', 'Critical')]))
    description = forms.CharField(
        widget=TinyMCE(
            attrs={
                'cols': 80,
                'rows': 30}),
        validators=[
            MinLengthValidator(
                1,
                message="This field cannot be empty")])

    class Meta:
        model = FlatPage


class CommentForm(forms.Form):
    commenter = forms.CharField(widget=forms.HiddenInput(), required=False)
    comment = forms.CharField(
        widget=TinyMCE(
            attrs={
                'cols': 80,
                'rows': 30}),
        required=True)
