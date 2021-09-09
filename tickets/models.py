from django.db import models
from django.conf import settings
from clients.models import Client, Contract


class Setup(models.Model):
    wrike_api_value = models.CharField(max_length=30)

    def __str__(self):
        return f'Settings'


class Ticket(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default='')
    issue = models.TextField()
    wrike_number = models.CharField(max_length=10)
    severity = models.CharField(
        max_length=2,
        choices=[
            ('ST', 'Standard'),
            ('HI', 'High'),
            ('VH', 'Very High'),
            ('CR', 'Critical')
        ]
    )
    # Future Machine Learning Opportunity
    hours_predicted = models.FloatField(default=0)
    # Required
    hours_used = models.FloatField(default=0)
    customer_feedback_requested = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    date_created = models.DateTimeField('Date Created')
    date_updated = models.DateTimeField('Date Updated', null=True)
    file_upload = models.FileField(null=True)

    def __str__(self):
        return f'{self.client} - {self.issue}'


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    sender = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    comment = models.TextField()
    date_sent = models.DateTimeField('Date Sent', blank=True)

    def __str__(self):
        return f'{self.ticket.issue} - {self.date_sent:%d-%m-%Y}'
