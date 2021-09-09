from django.db import models
from django.conf import settings

# Create your models here.


class Contract(models.Model):
    contract_name = models.CharField(
        max_length=5,
        choices=[
            ('30min', '30 Minutes Per Month'),
            ('1hour', '1 Hour Per Month'),
            ('2hour', '2 Hours Per Month'),
            ('4hour', '4 Hours Per Month'),
        ]
    )

    def __str__(self):
        return self.contract_name


class Client(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True)
    client_name = models.CharField(max_length=200)
    client_email = models.EmailField()
    client_address = models.CharField(max_length=200, null=True, blank=True)
    client_registered_company_number = models.CharField(
        max_length=30, null=True, blank=True)
    live_client = models.BooleanField(default=True)
    date_registered = models.DateTimeField('Date Registered')
    contract_type = models.ForeignKey(Contract, on_delete=models.CASCADE)
    contract_start_date = models.DateTimeField()
    contracted_monthly_service_hours = models.FloatField(default=2)
    contracted_monthly_SEM_hours = models.FloatField(default=2)
    paid_extra_hours = models.FloatField(default=0)
    hours_used_this_month = models.FloatField(default=0)
    discontented_client = models.BooleanField(default=False)
    priority_client = models.BooleanField(default=False)

    def __str__(self):
        return self.client_name
