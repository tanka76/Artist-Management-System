
from django.urls import path
from .views import ArtistListView,ArtistCreateView,ArtistUpdateView

app_name="artist"


urlpatterns = [

    path("artist/", ArtistListView.as_view(), name="artist_view"),
    path("artust/create/", ArtistCreateView.as_view(), name="artist_create_view"),
    path("artust/<int:pk>/update/", ArtistUpdateView.as_view(), name="artist_update_view"),


    
]

