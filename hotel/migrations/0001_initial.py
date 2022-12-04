# Generated by Django 4.1 on 2022-12-04 18:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=150)),
                ('check_in_date', models.DateField()),
                ('check_in_time', models.TimeField()),
                ('check_out_time', models.TimeField()),
                ('room_numbers', models.CharField(max_length=4000, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\ ,\\d+)*\\Z'), code='invalid', message=None)])),
                ('category', models.CharField(choices=[('Regular', 'Regular'), ('Executive', 'Executive'), ('Deluxe', 'Deluxe'), ('King', 'King'), ('Queen', 'Queen')], max_length=9)),
                ('person', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')], default=1)),
                ('no_of_rooms', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(1)])),
                ('room_managers', models.CharField(max_length=4000, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\ ,\\d+)*\\Z'), code='invalid', message=None)])),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_number', models.PositiveSmallIntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(1)])),
                ('category', models.CharField(choices=[('Regular', 'Regular'), ('Executive', 'Executive'), ('Deluxe', 'Deluxe'), ('King', 'King'), ('Queen', 'Queen')], max_length=9)),
                ('capacity', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')], default=2)),
                ('advance', models.PositiveSmallIntegerField()),
                ('room_manager', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['room_number'],
            },
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_from', models.TimeField()),
                ('available_till', models.TimeField()),
                ('room_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.room')),
            ],
        ),
    ]
