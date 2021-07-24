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

    tickets = Ticket.objects.filter(resolved = False).all().order_by('-date_created')
    return render(request,'tickets/admin/tickets.html', {'tickets': tickets})

def admin_tickets_single(request, number):
    if not request.user.is_authenticated:
        return redirect('/')
    if not request.user.is_staff:
        return redirect('/')

    ticket = Ticket.objects.filter(pk = number).first()
    comments = Comment.objects.filter(ticket = number).all().order_by('-date_sent')
    return render(request,'tickets/admin/ticket-single.html', {'ticket': ticket, 'comments': comments})

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
    tickets = Ticket.objects.all()
    contracts = Contract.objects.all()
    return render(request,'tickets/admin/companies.html', {'tickets':tickets, 'companies': companies})

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
    if request.user.is_staff:
        return redirect('/dashboard/admin/tickets/' + str(number))

    company = Client.objects.filter(user=request.user).first()
    ticket = Ticket.objects.filter(id=number).first()
    comments = Comment.objects.filter(ticket = ticket).all()
    if company.id != ticket.client.id:
        return redirect('/support')
    return render(request,'tickets/support/ticket.html', {'company': company, 'ticket': ticket, 'comments': comments})

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

def comment(request, number):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first()
    ticket = Ticket.objects.filter(pk = number).first()


    if company != ticket.client:
        if request.user.is_staff != True:
            return redirect('/')

    form = CommentForm({'commmenter': company.client_name, 'comment': '', 'file': '',})
    comments = Comment.objects.filter(ticket = number).all()
    return render(request,'tickets/comment.html', {'company':company, 'form':form, 'ticket': ticket, 'comments':comments,})

def comment_post(request, number):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first()
    ticket = Ticket.objects.filter(pk = number).first()

    if company != ticket.client:
        if request.user.is_staff != True:
            return redirect('/')

    if request.method == 'POST':
        newcomment = Comment()
        newcomment.ticket = ticket
        newcomment.sender = company
        newcomment.comment = request.POST['comment']
        newcomment.date_sent = datetime.now()
        newcomment.save()

    return redirect('/support/' + str(number))

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
