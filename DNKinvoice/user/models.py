from django.db import models
from django.contrib.auth.models import User


class UserData(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    full_name = models.CharField(max_length=255)
    phone_number = models.BigIntegerField()
    house_number = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=100)
    pincode = models.IntegerField()
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
