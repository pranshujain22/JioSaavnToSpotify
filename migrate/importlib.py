from traceback import print_exc
from migrate import saavn
import spotipy
import json


def get_songs_list(query):
    proxies = saavn.fate_proxy()
    data = dict()

    if '/album/' in query:
        print("Album")
        id = saavn.AlbumId(query, proxies)
        songs = saavn.getAlbum(id, proxies)
        songs_list = []
        for song in songs["songs"]:
            songs_list.append(song['song'])

        print(json.dumps(songs_list, indent=4))
        data = songs_list

    elif '/playlist/' or '/featured/' in query:
        print("Playlist")
        id = saavn.getListId(query, proxies)
        songs = saavn.getPlayList(id, proxies)
        songs_list = []
        for song in songs['songs']:
            songs_list.append(song['song'])

        print(json.dumps(songs_list, indent=4))
        data = songs_list

    return data


def get_folder_name(query):

    if '/album/' in query:
        print("Album")
        album_name = str(query).split('/')[-2]
        return album_name

    elif '/playlist/' or '/featured/' in query:
        print("Playlist")
        playlist_name = str(query).split('/')[-2]
        return playlist_name

    return 'sample_name'


def import_to_spotify(username, playlist_name, song_names_inside_playlist, token):
    try:
        spotify = spotipy.Spotify(auth=token)
        print('token: ', token)
        song_ids_acc_to_spotify = []

        print('length: ', len(song_names_inside_playlist))
        for song_names in song_names_inside_playlist:
            results = spotify.search(q=song_names, limit=1, offset=0, type='track', market=None)
            if len(results["tracks"]["items"]) != 0:
                results = results["tracks"]["items"][0]["id"]
                song_ids_acc_to_spotify.append(str(results))

        print(song_ids_acc_to_spotify)

        # ------------------------------------------------------------------------------------

        current_playlist_id = spotify.user_playlist_create(str(username), playlist_name, public=True,
                                                           description='')
        current_playlist_id = str(current_playlist_id["id"])
        while song_ids_acc_to_spotify:
            spotify.user_playlist_add_tracks(str(username), current_playlist_id, song_ids_acc_to_spotify[:100], None)
            song_ids_acc_to_spotify = song_ids_acc_to_spotify[100:]
    except:
        print_exc()
        return False

    return True

