# Generated by Django 4.0.3 on 2022-06-08 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='user',
            field=models.CharField(max_length=30),
        ),
    ]