# Generated by Django 3.1.7 on 2021-03-24 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('trx_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('post_balance', models.FloatField()),
                ('trx_type', models.CharField(choices=[('DEPOSIT', 'Deposit'), ('WITHDRAW', 'Withdraw')], max_length=255)),
                ('trx_status', models.CharField(choices=[('PROCESSING', 'Processing'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')], default='PROCESSING', max_length=255)),
                ('trx_date', models.DateField(auto_now_add=True)),
                ('payment_method', models.CharField(choices=[('PERFECT_MONEY', 'Perfect Money'), ('COIN_PAYMENT', 'Coin Payment')], max_length=255)),
                ('amount', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
