from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime


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
    if request.user.is_staff:
        return redirect('/dashboard/admin')

    company = Client.objects.filter(user=request.user).first()
    return render(request,'tickets/dashboard.html', {'company':company})

def dashboard_admin(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if not request.user.is_staff:
        return redirect('/')

    return render(request,'tickets/admindashboard.html', {})

def admin_tickets(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if not request.user.is_staff:
        return redirect('/')

    return render(request,'tickets/admindashboard.html', {})

def admin_search(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if not request.user.is_staff:
        return redirect('/')

    return render(request,'tickets/admindashboard.html', {})

def admin_companies(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if not request.user.is_staff:
        return redirect('/')

    companies = Client.objects.all()
    tickets = Ticket.objects.filter(resolved = False).all()
    return render(request,'tickets/admin/companies.html', {'tickets':tickets, 'companies': companies})

def admin_log(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if not request.user.is_staff:
        return redirect('/')

    companies = Client.objects.all()
    tickets = Ticket.objects.filter(resolved = False).all()
    return render(request,'tickets/admin/log.html', {'tickets':tickets, 'companies': companies})

def account(request):

    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first()
    return render(request,'tickets/account.html', {'company': company, })

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

def notificationsettings(request):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first()
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

    company = Client.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = NewTicketForm(request.POST)
        if form.is_valid():
            newticket = Ticket()
            newticket.client = company
            newticket.title= request.POST['subject']
            newticket.severity = request.POST['priority']
            newticket.issue = request.POST['description']
            newticket.date_created = datetime.now()
            newticket.date_updated = datetime.now()
            newticket.save()
            return redirect('/support')
    form = NewTicketForm()
    return render(request,'tickets/report.html', {'company':company, 'form':form})

def support(request):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first()
    tickets = Ticket.objects.filter(client__exact=company.id)
    return render(request,'tickets/support.html', {'company':company, 'tickets':tickets})

def supportticket(request, number):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first()
    ticket = Ticket.objects.filter(id=number).first()
    if company.id != ticket.client.id:
        return redirect('/support')
    return render(request,'tickets/support/ticket.html', {'company': company, 'ticket': ticket})

def editticket(request, number):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first()
    ticket = Ticket.objects.filter(id = number).first()
    if request.method == 'POST':
        form = NewTicketForm(request.POST)
        if form.is_valid():
            ticket.client = company
            ticket.title= request.POST['subject']
            ticket.severity = request.POST['priority']
            ticket.issue = request.POST['description']
            ticket.date_updated = datetime.now()
            ticket.save()
            return redirect('/support/' + str(ticket.id))
    form = NewTicketForm({'subject': ticket.title, 'priority': ticket.severity, 'description': ticket.issue, 'category': 'Normal',})
    return render(request,'tickets/support/edit.html', {'company':company, 'form':form, 'ticket': ticket})

def markticket(request, number):
    if not request.user.is_authenticated:
        return redirect('/')

    ticket = Ticket.objects.filter(id = number).first()
    if ticket.resolved == True:
        ticket.resolved = False
    else:
        ticket.resolved = True
    ticket.save()
    return redirect('/support')

def contact(request):
    return render(request,'tickets/contact.html', {})

def buy(request):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first()
    return render(request,'tickets/buy.html', {'company':company})

def logout_view(request):
        logout(request)
        return redirect('/')
