# Generated by Django 3.1.7 on 2021-03-28 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_remove_transaction_trx_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='trx_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
