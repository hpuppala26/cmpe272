from django.contrib import admin
from .models import Interest_Model,Pending_Requests,Confirmed_Friends
# Register your models here.
admin.site.register(Interest_Model)
admin.site.register(Pending_Requests)
admin.site.register(Confirmed_Friends)
