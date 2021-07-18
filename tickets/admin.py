from django.contrib import admin

from .models import *

admin.site.register(Client)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Contract)
admin.site.register(Setup)
