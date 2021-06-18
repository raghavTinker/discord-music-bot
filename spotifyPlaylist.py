import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import os

auth_manager = None
sp = None
id = ""
secret = ""
def getSpotifySongs(url):
    playlist_id = url.split("/")[4].split("?")[0]
    playlist = sp.playlist(playlist_id=playlist_id)
    
    songs = []
    for item in playlist["tracks"]["items"]:
        track_id = item["track"]["id"]
        info = sp.track(track_id)

        songs.append(info['name'] + ", " + info['album']['artists'][0]['name'])
    
    print(songs)
    return songs

def getSpotifySong(url):
    track_id = url.split("/")[4].split("?")[0]
    song = sp.track(track_id=track_id)
    name = song['name']
    artist = song['album']['artists'][0]['name']

    return name + ", " + artist

def albumTracks(url):
    album_id = url.split("/")[4].split("?")[0]
    album = sp.album(album_id=album_id)
    songs = []
    for item in album["tracks"]["items"]:
        artist = item["artists"][0]["name"]
        track = item["name"]
        songs.append(track + ", " + artist)
    return songs
try:
    id = str(os.environ['SPOTIFY_ID'])
    secret = str(os.environ['SPOTIFY_SECRET'])
    print(id)
    print(secret)
    auth_manager = SpotifyClientCredentials(client_id=id, client_secret=secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except:
    print("Invalid keys")


