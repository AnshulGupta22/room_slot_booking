from django.db import models

# Create your models here.

class Hotel(models.Model):
    username = models.CharField(max_length=120)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField()

