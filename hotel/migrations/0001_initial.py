# Generated by Django 4.0.3 on 2022-06-14 19:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=30)),
                ('book_from_date', models.DateField()),
                ('book_from_time', models.TimeField()),
                ('book_till_time', models.TimeField()),
                ('room_number', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('category', models.CharField(choices=[('YAC', 'AC'), ('NAC', 'NON-AC'), ('DEL', 'DELUXE'), ('KIN', 'KING'), ('QUE', 'QUEEN')], max_length=3)),
                ('capacity', models.CharField(choices=[('one', '1'), ('two', '2'), ('thr', '3'), ('fou', '4')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(1)])),
                ('available_from', models.TimeField()),
                ('available_till', models.TimeField()),
                ('advance', models.PositiveSmallIntegerField()),
                ('category', models.CharField(choices=[('YAC', 'AC'), ('NAC', 'NON-AC'), ('DEL', 'DELUXE'), ('KIN', 'KING'), ('QUE', 'QUEEN')], max_length=3)),
                ('capacity', models.CharField(choices=[('one', '1'), ('two', '2'), ('thr', '3'), ('fou', '4')], max_length=3)),
            ],
        ),
    ]
