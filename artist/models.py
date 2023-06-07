from django.db import models
from artist_management_system.utils import BaseModel

# Create your models here.
from users.models import GENDER_CHOICES

GENRE_CHOICES = (
        ('RNB', 'RNB'),
        ('COUNTRY', 'COUNTRY'),
        ('CLASSIC', 'CLASSIC'),
        ('ROCK', 'ROCK'),
        ('JAZZ', 'JAZZ'),
    )

class Artist(BaseModel):
    name=models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES,default='M')
    dob=models.DateTimeField(verbose_name='Date of Birth',null=True,blank=True)
    first_release_year=models.DateField(null=True,blank=True)
    number_of_albums_released=models.PositiveIntegerField(null=True,blank=True)


    def __str__(self):
        return self.name
    
    # def first_release_year(self):
    #     return self.first_release_year

    

class Music(BaseModel):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE,related_name="music")
    title=models.CharField(max_length=255)
    album_name=models.CharField(max_length=255)
    genre=models.CharField(max_length=20, choices=GENRE_CHOICES,default='RNB')


    def __str__(self):
        return self.title
    
    
