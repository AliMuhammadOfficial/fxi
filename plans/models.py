from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal, getcontext

class Plan(models.Model):
    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    PERIOD = (
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly')
    )

    LIFE_TIME = 'LIFE_TIME'
    YEARLY = 'YEARLY'
    PLAN_PERIOD = (
        (LIFE_TIME, 'Life Time'),
        (YEARLY, 'Year (260 Days)')
    )
    plan_id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    minimum = models.FloatField()
    maximum = models.FloatField()
    roi = models.CharField(max_length=255, default='')
    roi_period = models.CharField(max_length=255, choices=PERIOD, default=DAILY)
    plan_period = models.CharField(max_length=255, choices=PLAN_PERIOD, default=LIFE_TIME)
    capital_return = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    def __str__(self):
        return self.name
        
    
class RoiAmount(models.Model):
    roi_id = models.AutoField(primary_key=True, unique=True)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    percent = models.DecimalField(
        max_digits = 12,
        decimal_places = 3
    )

    def __str__(self):
        getcontext().prec = 2
        return "{:.1f}%".format(float(self.percent) * 100)
    

class Investment(models.Model):

    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    EXPIRED = 'EXPIRED'
    STATUS_CHOICE = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (EXPIRED, 'Expired')
    )
    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    PERIOD = (
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly')
    )
    investment_id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    amount = models.FloatField()
    interest = models.FloatField(default=0.00)
    period = models.CharField(max_length=255, choices=PERIOD, default=DAILY)
    next_time = models.DateTimeField(auto_now_add=True)
    last_time = models.DateTimeField(auto_now=False, editable=False, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICE, default=INACTIVE)
    return_capital = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return f"{self.user}-{self.plan}"