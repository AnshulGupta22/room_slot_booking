# Generated by Django 4.1 on 2022-10-02 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0004_alter_booking_person_alter_room_capacity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerapi',
            old_name='confirm_password',
            new_name='retype_password',
        ),
    ]