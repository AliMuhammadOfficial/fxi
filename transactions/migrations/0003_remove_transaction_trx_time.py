# Generated by Django 3.1.7 on 2021-03-28 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20210328_2230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='trx_time',
        ),
    ]