# Generated by Django 4.2.3 on 2023-12-03 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LPSApp', '0016_alter_order_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
