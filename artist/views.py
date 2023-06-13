import csv
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages


from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView,CreateView,TemplateView,UpdateView,ListView,View,DetailView
from users.permissions import IsLoggedInMixin,is_logged_in
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
@is_logged_in
def upload_csv(request, pk):
    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")
        if not csv_file.name.endswith(".csv"):
            print("Invalid Format===============")
            messages.error(request, "Invalid Format")
        with open(csv_file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                artist = Artist.objects.create(name=row[0],address=row[1],gender=row[2],dob=row[3],number_of_albums_released=row[4],first_release_year=row[5])                
                artist.save() 
        messages.success(request, "Succesfully Uplaod Csv file")
    return redirect(request.META.get("HTTP_REFERER"))


@is_logged_in
def export_to_csv(request):
    if request.method == "GET":
        try:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="artist.csv"'
            writer = csv.writer(response)
            writer.writerow(['name', 'address','dob','gender','number_of_albums_released','first_release_year'])  
            artists = Artist.objects.filter(is_deleted=False) 
            for artist in artists:
                writer.writerow([artist.name, artist.address, artist.dob,artist.gender,artist.number_of_albums_released,artist.first_release_year])
        except Exception as e:
            print("Error",e)

        return response
