# Generated by Django 3.1.7 on 2021-04-04 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_auto_20210404_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=3, max_digits=12),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='post_balance',
            field=models.DecimalField(decimal_places=3, max_digits=12),
        ),
    ]
