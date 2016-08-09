from django.http import HttpResponse
from .models import Album


def index(request):
    all_albums = Album.objects.all()
    html = ''
    for album in all_albums:
        url = '%d/' % album.id
        html += '<a href="%s">%s</a><br>' % (url,album.album_title)
    return HttpResponse(html)


def detail(request, album_id):
    return HttpResponse("<h2>Details for Album id: %s </h2" % str(album_id))
