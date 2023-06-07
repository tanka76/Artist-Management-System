
from django.urls import path
from .views import ArtistListView,ArtistCreateView,ArtistUpdateView,ArtistDeleteView,ArtistDetailView,MusicCreateView,MusicDeleteView,MusicUpdateView

app_name="artist"


urlpatterns = [

    path("artist/", ArtistListView.as_view(), name="artist_view"),
    path("artist/create/", ArtistCreateView.as_view(), name="artist_create_view"),
    path("artist/<int:pk>/update/", ArtistUpdateView.as_view(), name="artist_update_view"),
    path("artist/<int:pk>/delete/", ArtistDeleteView.as_view(), name="artist_delete_view"),
    path("artist/detail/<int:pk>/",ArtistDetailView.as_view(),name="artist_detail_view"),

    #songs
    path("music/<int:pk>/create/", MusicCreateView.as_view(), name="music_create_view"),
    path("music/<int:pk>/update/", MusicUpdateView.as_view(), name="music_update_view"),
    path("music/<int:pk>/delete/", MusicDeleteView.as_view(), name="music_delete_view"),



    
]

