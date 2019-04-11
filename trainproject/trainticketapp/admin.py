from django.contrib import admin
from trainticketapp.models import TicketPreference

# Register your models here.

class TicketPreferenceAdmin(admin.ModelAdmin):
    list_display=('name','age','gender','berth_preference','rac_seats','waiting_list')

admin.site.register(TicketPreference,TicketPreferenceAdmin)
