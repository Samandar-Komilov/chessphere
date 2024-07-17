from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django_countries.fields import CountryField

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(blank=True, null=True)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3000)], default=800, blank=True, null=True)
    country = CountryField(blank=True, null=True)


    def __str__(self):
        return self.user.username
