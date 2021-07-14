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

    company = Client.objects.filter(user=request.user).first
    return render(request,'tickets/dashboard.html', {'company':company})

def account(request):

    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first
    return render(request,'tickets/account.html', {'company': company, })

def passwordupdate(request):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first
    return render(request,'tickets/account/passwordupdate.html', {'company':company})

def notificationsettings(request):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first
    return render(request,'tickets/account/notificationsettings.html', {'company':company})

def privacy(request):
    return render(request,'tickets/privacy.html', {})

def copyright(request):
    return render(request,'tickets/copyright.html', {})

def terms(request):
    return render(request,'tickets/terms.html', {})

def report(request):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first
    return render(request,'tickets/report.html', {'company':company})

def support(request):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first
    return render(request,'tickets/support.html', {'company':company})

def supportticket(request, number):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first
    return render(request,'tickets/support/ticket.html', {'company':company})

def contact(request):
    return render(request,'tickets/contact.html', {})

def buy(request):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first
    return render(request,'tickets/buy.html', {'company':company})

def logout_view(request):
        logout(request)
        return redirect('/')
