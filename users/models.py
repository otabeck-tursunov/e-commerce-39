from django.db import models
from django.contrib.auth.models import AbstractUser
from cities_light.models import Country


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to="users/", blank=True, null=True)
    gender = models.CharField(max_length=20, choices=(("erkak", "erkak"), ("ayol", "ayol")))
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)
    confirmed = models.BooleanField(default=False)

    def in_login(self):
        return self.confirmed and self.is_authenticated


    
