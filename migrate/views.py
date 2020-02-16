from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from migrate import importlib
import json


SPOTIPY_CLIENT_ID = "85afea4742854bdd8d958433a89f229c"
SPOTIPY_REDIRECT_URI = "https://github.com/pranshujain22/"
SPOTIPY_SCOPE = "playlist-read-private"
SPOTIFY_AUTH_END_POINT = "https://accounts.spotify.com/authorize?" + \
                         "client_id=" + SPOTIPY_CLIENT_ID + \
                         "&redirect_uri=" + SPOTIPY_REDIRECT_URI + \
                         "&scope=" + SPOTIPY_SCOPE + \
                         "&response_type=token"


# Create your views here.
def index(request):
    if request.method == 'GET':
        return render(request, 'migrate/index.html')


def get_auth_details(request):
    if request.method == 'GET':
        return JsonResponse({'auth_endpoint': SPOTIFY_AUTH_END_POINT})


def spotify_auth(request):
    return render(request, 'migrate/spotifyAuth.html')


@csrf_exempt
def import_playlist(request):
    if request.method == 'POST':
        query = request.POST.get('playlistLink')
        username = request.POST.get('id')
        token = request.POST.get('token')

        songs_list = importlib.get_songs_list(query)
        print('songs_list: ', songs_list)
        folder_name = importlib.get_folder_name(query)
        print('folder_name: ', folder_name)
        if importlib.import_to_spotify(username, folder_name, songs_list, token):
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse({'message': 'falied'})

    return JsonResponse({})
