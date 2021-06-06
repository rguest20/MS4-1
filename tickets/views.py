from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views import View
from .models import *


def index(request):
    return render(request,'tickets/index.html')


def access(request):
    template = loader.get_template('login.html')
    context = {}
    return render(request,'tickets/login.html')
