from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from datetime import datetime, timezone
import stripe
import json
from django.contrib.auth import get_user_model


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard/')
    else:
        return redirect('/login')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.user.is_staff:
        return redirect('/dashboard/admin')
    try:
        company = Client.objects.filter(user=request.user).first()
        total_hours = company.paid_extra_hours + company.contracted_monthly_SEM_hours + company.contracted_monthly_service_hours - company.hours_used_this_month
    except:
        messages.error(request, 'This functionality will not work until you have been assigned to a company.  Please wait, our admins will assign you soon.')
        return redirect('/logout')
    return render(request,'tickets/dashboard.html', {'company':company, 'hours': total_hours})

def dashboard_admin(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if not request.user.is_staff:
        return redirect('/')

    tickets = Ticket.objects.filter(resolved = False).all()
    unresolved = Ticket.objects.filter(resolved = False).all()
    weekold = []
    for ticket in tickets:
        d = ticket.date_created
        now = datetime.now(timezone.utc)
        if (d - now).days > 7:
            weekold.append(ticket)
    return render(request,'tickets/admindashboard.html', {'unresolved': unresolved, 'weekold': weekold})

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
    if request.user.is_staff:
        return redirect('/dashboard/admin')

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

def logout_view(request):
        logout(request)
        return redirect('/')
