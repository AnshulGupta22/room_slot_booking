from django.db import models

# Create your models here.

class Hotel(models.Model):
    username = models.CharField(max_length=120)
    email = models.EmailField()
    password = models.CharField(max_length=120)
