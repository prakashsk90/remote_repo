from django.db import models

# Create your models here.

class TicketPreference(models.Model):
    name=models.CharField(max_length=256)
    age=models.IntegerField()
    gender=models.CharField(max_length=10)
    berth_preference=models.CharField(max_length=256)
    rac_seats=models.CharField(max_length=10)
    waiting_list=models.CharField(max_length=10)
