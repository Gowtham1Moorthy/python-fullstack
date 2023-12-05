# Generated by Django 4.2.3 on 2023-12-03 04:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LPSApp', '0013_remove_order_number_6_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='powerball',
        ),
        migrations.AddField(
            model_name='order',
            name='winning_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(9999999999.99)]),
        ),
    ]
