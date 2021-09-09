from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from clients.models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from datetime import datetime, timezone
from django.contrib.auth import get_user_model


# Create your views here.
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
                return HttpResponseRedirect('/dashboard')
            else:
                messages.error(request, 'Invalid Username/Password')
                form = LoginForm()
                return render(request, 'tickets/index.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'tickets/index.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')

    if request.method == 'POST':
        form = RegisterUserCompany(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        repeat_password = request.POST['repeat_password']
        email = request.POST['company_email']
        name = request.POST['company_name']
        address = request.POST['business_address']
        registration = request.POST['company_registration_number']
        contract = request.POST['contract']
        if password != repeat_password:
            messages.error(request, 'Passwords do not match')
            return redirect('/login/register')
        else:
            safepassword = make_password(password)
            newcontract = Contract.objects.filter(
                contract_name=contract).first()
            User = get_user_model()
            newuser = User()
            newuser.username = username
            newuser.password = safepassword
            newuser.save()
            newclient = Client()
            newclient.user = newuser
            newclient.client_name = name
            newclient.client_email = email
            newclient.address = address
            newclient.client_registered_company_number = registration
            newclient.live_client = True
            newclient.date_registered = datetime.now()
            newclient.contract_type = newcontract
            newclient.contract_start_date = datetime.now()
            newclient.save()
            login(request, newuser)
            return redirect('/')

    else:
        form = RegisterUserCompany()
        return render(request, 'tickets/register.html', {'form': form})
