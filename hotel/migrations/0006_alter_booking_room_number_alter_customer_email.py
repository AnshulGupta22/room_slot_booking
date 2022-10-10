# Generated by Django 4.1 on 2022-10-03 20:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0005_rename_confirm_password_customerapi_retype_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='room_number',
            field=models.PositiveSmallIntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]