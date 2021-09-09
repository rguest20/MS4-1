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
from tickets.models import Client
from emc_tickets import settings


def buy(request):
    if not request.user.is_authenticated:
        return redirect('/')

    company = Client.objects.filter(user=request.user).first()

    return render(request, 'tickets/buy.html', {'company': company})


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
            # For full details see
            # https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url +
                'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url +
                'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                client_reference_id=request.user.username,
                line_items=[
                    {
                        'quantity': dict,
                        'price_data': {
                            'currency': 'GBP',
                            'product': 'prod_JutS7RlYuaxtDj',
                            'unit_amount': productprice.unit_amount}}])
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def cancelled(request):
    return render(request, 'tickets/stripe/cancelled.html', {})


def success(request):
    return render(request, 'tickets/stripe/success.html', {})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'checkout.session.completed':
        session = event.data.object
        hoursbought = session.amount_total / 10000
        customer_email = session.customer_details.email
        User = get_user_model()
        userrequested = User.objects.filter(username = session.client_reference_id).first()
        customer = Client.objects.filter(
            user= userrequested).first()
        customer.paid_extra_hours += hoursbought
        customer.save()
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)
