# Generated by Django 4.1 on 2022-10-20 17:40

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0006_alter_booking_room_number_alter_customer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='no_of_rooms',
            field=models.CharField(max_length=9, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
    ]
