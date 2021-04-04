from django.db import models
from django.conf import settings
import datetime
from django.utils import timezone

class Transaction(models.Model):

    PERFECT_MONEY = 'PERFECT_MONEY'
    COIN_PAYMENT = 'COIN_PAYMENT'
    PAYMENT_CHOICES = (
        (PERFECT_MONEY, 'Perfect Money'),
        (COIN_PAYMENT, 'Coin Payment'),
    )
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'
    TRX_TYPE = (
        (DEPOSIT, 'Deposit'),
        (WITHDRAW, 'Withdraw'),
    )
    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    TRX_STATUS = (
        (PROCESSING, 'Processing'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed')
    )
    trx_id = models.AutoField(primary_key=True, unique=True, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    post_balance = models.FloatField(null=False)
    trx_type = models.CharField(max_length=255, choices=TRX_TYPE)
    trx_status = models.CharField(max_length=255, choices=TRX_STATUS, default=PROCESSING)
    trx_date = models.DateField(auto_now_add=True)
    trx_time = models.TimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_CHOICES)
    amount = models.FloatField(null=False)
    def __str__(self):
        return f"TRX-{self.trx_id}"

