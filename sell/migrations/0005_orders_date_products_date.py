# Generated by Django 4.1.5 on 2023-02-09 04:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sell', '0004_orders_price_alter_orders_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 9, 10, 23, 47, 936438)),
        ),
        migrations.AddField(
            model_name='products',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 9, 10, 23, 47, 936438)),
        ),
    ]
