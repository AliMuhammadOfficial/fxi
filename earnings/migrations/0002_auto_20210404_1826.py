# Generated by Django 3.1.7 on 2021-04-04 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('earnings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earnings',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]
