import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from artist_management_system.utils import BaseForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from .models import Artist,Music

class ArtistForm(BaseForm,forms.ModelForm):
    class Meta:
        model = Artist
        fields = [
            "name",
            "address",
            "gender",
            "dob",
            "first_release_year",
            "number_of_albums_released"

        ]

class MusicForm(BaseForm,forms.ModelForm):
    class Meta:
        model = Music
        fields = [
            "title",
            "album_name",
            "genre"


        ]