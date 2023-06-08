from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView,CreateView,TemplateView,UpdateView,ListView,View,DetailView
from users.permissions import IsLoggedInMixin
from .models import Artist,Music
from .forms import ArtistForm,MusicForm

# Create your views here.

class ArtistMixin(IsLoggedInMixin):
    model = Artist
    paginate_by = 10
    queryset = Artist.objects.filter(is_deleted=False)
    success_url = reverse_lazy("artist:artist_view")


class ArtistListView(ArtistMixin, ListView):
    template_name = "artist_list.html"
    queryset = Artist.objects.filter(is_deleted=False)
    paginate_by = 4



class ArtistCreateView(ArtistMixin, CreateView):
    form_class = ArtistForm
    template_name = "artist_create.html"

class ArtistUpdateView(ArtistMixin, UpdateView):
    form_class = ArtistForm
    template_name = "update.html"


class ArtistDeleteView(View):

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Artist, pk=kwargs['pk'])
        obj.is_deleted = True
        obj.save()
        return redirect(reverse_lazy("artist:artist_view"))
    

class ArtistDetailView(ArtistMixin,DetailView):
    template_name = "artist_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artist=Artist.objects.get(id=self.kwargs.get('pk'))
        context['music_list']=Music.objects.filter(artist=artist,is_deleted=False)
        return context
    


class MusicMixin(IsLoggedInMixin):
    model = Music
    paginate_by = 10
    queryset = Music.objects.filter(is_deleted=False)


class MusicCreateView(MusicMixin, CreateView):
    form_class = MusicForm
    template_name = "music_create.html"


    def form_valid(self, form):
        artist=Artist.objects.get(id=self.kwargs.get('pk'))
        form.instance.artist=artist
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            "artist:artist_detail_view",
            kwargs={"pk": self.kwargs.get('pk')},
        )

class MusicUpdateView(MusicMixin, UpdateView):
    form_class = MusicForm
    template_name = "update.html"


    def get_success_url(self):
        obj = get_object_or_404(Music, pk=self.kwargs.get('pk'))
        return reverse_lazy(
            "artist:artist_detail_view",
            kwargs={"pk": obj.artist.id},
        )

class MusicDeleteView(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Music, pk=kwargs['pk'])
        obj.is_deleted = True
        obj.save()
        return redirect(reverse_lazy("artist:artist_detail_view",kwargs={"pk": obj.artist.id}))


#csv import export views