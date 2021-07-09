from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('dashboard/')
            else:
                messages.error(request, 'Invalid Username/Password')
                form = LoginForm()
                return render(request,'tickets/index.html', {'form': form})
    else:
        form = LoginForm()
        return render(request,'tickets/index.html', {'form': form})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/')
    return render(request,'tickets/dashboard.html', {})

def account(request):
    return render(request,'tickets/account.html', {})

def passwordupdate(request):
    return render(request,'tickets/account/passwordupdate.html', {})

def notificationsettings(request):
    return render(request,'tickets/account/notificationsettings.html', {})

def privacy(request):
    return render(request,'tickets/privacy.html', {})

def privacy(request):
    return render(request,'tickets/copyright.html', {})

def terms(request):
    return render(request,'tickets/terms.html', {})

def report(request):
    return render(request,'tickets/report.html', {})

def support(request):
    return render(request,'tickets/support.html', {})

def supportticket(request):
    return render(request,'tickets/support/ticket.html', {})

def contact(request):
    return render(request,'tickets/contact.html', {})

def buy(request):
    return render(request,'tickets/buy.html', {})

def logout_view(request):
        logout(request)
        return redirect('/')
