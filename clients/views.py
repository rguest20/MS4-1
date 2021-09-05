from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import *
from tickets.models import *
from .forms import * 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from datetime import datetime, timezone
import stripe
import json
from django.contrib.auth import get_user_model

# Create your views here.
def admin_companies(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if not request.user.is_staff:
        return redirect('/')

    companies = Client.objects.all()
    tickets = Ticket.objects.all()
    contracts = Contract.objects.all()
    User = get_user_model()
    users = User.objects.all()
    userstoremove = []
    for company in companies:
        if company.user in users:
            userstoremove.append(company.user.username)
            finalusers = User.objects.all().exclude(username__in = userstoremove)
    form = CreateNewUser()
    return render(request,'tickets/admin/companies.html', {'tickets':tickets, 'companies': companies, 'users': finalusers, 'form': form})

def admin_log(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if not request.user.is_staff:
        return redirect('/')

    companies = Client.objects.all()
    tickets = Ticket.objects.filter(resolved = False).all()

    if request.method == 'POST':
        ticket = Ticket.objects.filter(title = request.POST['ticket']).first()
        ticketclient = ticket.client
        ticketclient.hours_used_this_month = ticketclient.hours_used_this_month + float(request.POST['hours'])
        ticket.hours_used = ticket.hours_used + float(request.POST['hours'])
        ticket.save()
        ticketclient.save()
        return redirect('/dashboard/admin')
    return render(request,'tickets/admin/log.html', {'tickets':tickets, 'companies': companies})

def admin_create_user(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if not request.user.is_staff:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        safepassword = make_password(password)
        User = get_user_model()
        newuser = User()
        newuser.username = username
        newuser.password = safepassword
        newuser.save()
        return render(request, 'tickets/admin/usercreated.html', {'newuser': newuser})
    else:
        return redirect('/')

def admin_create_company(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if not request.user.is_staff:
        return redirect('/')

    if request.method == 'POST':
        companyname = request.POST['companycreate']
        username = request.POST['companyassociate']
        User = get_user_model()
        user = User.objects.filter(username = username).first()
        contract = Contract.objects.first()
        newclient = Client()
        newclient.client_name = companyname
        newclient.user = user
        newclient.email = user.email
        newclient.live_client = True
        newclient.date_registered = datetime.now()
        newclient.contract_type = contract
        newclient.contract_start_date = datetime.now()
        newclient.save()
        return render(request, 'tickets/admin/companycreated.html', {'newcompany': newclient})
    else:
        return redirect('/')

def delete(request):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first()
    company.delete()
    return redirect('/deleted')

def deleted(request):
    return render(request,'tickets/deleted.html', {})

def account(request):

    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first()
    return render(request,'tickets/account.html', {'company': company, })

def account_edit(request):

    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = AccountUpdateForm(request.POST)
        if form.is_valid():
            company.client_name = request.POST['company_name']
            company.client_address = request.POST['address']
            company.client_registered_company_number = request.POST['company_registration_number']
            company.client_email = request.POST['company_email']
            company.save()
            return redirect('/account')
    form = AccountUpdateForm({'company_name': company.client_name,'address': company.client_address,'company_registration_number': company.client_registered_company_number,'company_email': company.client_email,})
    return render(request,'tickets/account/edit.html', {'company': company, 'form': form})

def passwordupdate(request):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            oldpassword = request.POST['current_password']
            new_password = request.POST['new_password']
            verification = request.POST['please_reenter_new_password']
            if condition:
                pass
    return render(request,'tickets/account/passwordupdate.html', {'company':company})
