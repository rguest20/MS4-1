from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
import stripe
import json


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
    total_hours = company.paid_extra_hours + company.contracted_monthly_SEM_hours + company.contracted_monthly_service_hours - company.hours_used_this_month
    return render(request,'tickets/dashboard.html', {'company':company, 'hours': total_hours})

def dashboard_admin(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if not request.user.is_staff:
        return redirect('/')

    tickets = Ticket.objects.all()
    unresolved = Ticket.objects.filter(resolved = False).all()
    for ticket in tickets:
        d = ticket.date_created # Add .date() if hour doesn't matter
        now = datetime.now()                 # Add .date() if hour doesn't matter
        if (d - now).days > 7:
            tickets.remove(ticket)
    return render(request,'tickets/admindashboard.html', {'unresolved': unresolved, 'weekold': tickets})

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

def delete(request):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first()
    company.delete()
    return redirect('/deleted')

def deleted(request):
    return render(request,'tickets/deleted.html', {})

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

def buy(request):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first()

    return render(request,'tickets/buy.html', {'company':company})

def logout_view(request):
        logout(request)
        return redirect('/')

def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        dict = request.POST.get('quantity', 1)
        domain_url = 'https://ms4-rguest.herokuapp.com/'
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        productprice = stripe.Price.retrieve(
            "price_1JH3fEDXIY8lmqgTKTREcxUO",
        )
        try:
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[{'quantity': dict, 'price_data': {'currency': 'GBP', 'product': 'prod_JutS7RlYuaxtDj', 'unit_amount': productprice.unit_amount}}]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

def cancelled(request):
    return render(request,'tickets/stripe/cancelled.html', {})

def success(request):
    return render(request,'tickets/stripe/success.html', {})

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        hoursbought = session.amount_total / 10000
        customer_email = session["customer_details"]["email"]
        customer = Client.objects.filter(client_email = customer_email).first()
        customer.paid_extra_hours += hoursbought
        customer.save()

    return HttpResponse(status=200)
