from django.contrib.gis.db import models
from .managers import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from globechain import constants

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):

    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['password']

    objects = UserManager()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,unique=False)
    last_name = models.CharField(max_length=100,unique=False)
    full_address = models.CharField(max_length=100,unique=False)
    location = models.PointField(blank=False)
    account_type = models.CharField(max_length=2,choices=constants.ACCOUNT_TYPES)

    class Meta:
        db_table = 'profile'