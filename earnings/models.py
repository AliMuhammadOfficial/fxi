from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Earnings(models.Model):
    ROI = 'ROI'
    REFERRAL_BONUS = 'REFERRAL_BONUS'
    AMBASSADOR_SALARY = 'AMBASSADOR_SALARY'
    EARNING_TYPE = (
        (ROI, 'ROI'),
        (REFERRAL_BONUS, 'Referral Bonus'),
        (AMBASSADOR_SALARY, 'Ambassador Salary')
    )
    earnings_id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT)
    earning_type = models.CharField(max_length=255, choices=EARNING_TYPE)
    amount = models.DecimalField(max_digits=12, decimal_places=3)

    def __str__(self):
        return self.earning_type
