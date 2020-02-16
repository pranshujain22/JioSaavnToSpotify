from django.urls import path
from migrate import views

# TEMPLATE TAGGING
app_name = 'migrate'

urlpatterns = [
    path('', views.index, name='index'),
    path('getAuthDetails', views.get_auth_details, name='getAuthDetails'),
    path('importPlaylist', views.import_playlist, name='importPlaylist'),
    path('spotifyAuth', views.spotify_auth, name='spotifyAuth')
]
