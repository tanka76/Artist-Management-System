from django.db import models
from django.contrib.auth.models import AbstractUser
from artist_management_system.utils import BaseModel


GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

class AuthUser(BaseModel,AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=False, unique=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    dob=models.DateTimeField(verbose_name='Date of Birth',null=True,blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES,default='M')


    def __str__(self):
        return self.email