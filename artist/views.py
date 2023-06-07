from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView,CreateView,TemplateView,UpdateView,ListView,View
from users.permissions import IsLoggedInMixin
from .models import Artist,Music
from .forms import ArtistForm

# Create your views here.

class ArtistMixin(IsLoggedInMixin):
    model = Artist
    paginate_by = 10
    queryset = Artist.objects.filter(is_deleted=False)
    success_url = reverse_lazy("artist:artist_view")


class ArtistListView(ArtistMixin, ListView):
    template_name = "artist_list.html"
    queryset = Artist.objects.filter(is_deleted=False)


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