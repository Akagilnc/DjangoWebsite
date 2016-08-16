from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .models import Album, Song
from django.contrib.auth import authenticate, login
from django.views.generic import View
from.forms import UserForm


def get_all_albums():
    return Album.objects.all()


class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return get_all_albums


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate(CreateView):
    model = Album
    template_name = 'music/album-form.html'
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumUpdate(UpdateView):
    model = Album
    template_name = 'music/album-form.html'
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form': form})


def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except(KeyError, Song.DoesNotExist):
        return render(request, 'music/detail.html',{
            'album': song.id,
            'error_message': "You did not select a valid song",
        })
    else:
        return render(request, 'music/detail.html', {'album': song.album})


def favorite_album(request, album_id):

    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except(KeyError, Album.DoesNotExist):
        return render(request, 'music/index.html',{
            'album': album.id,
            'error_message': "You did not select a valid album",
        })
    else:
        return render(request, 'music/index.html', {'all_albums': get_all_albums})