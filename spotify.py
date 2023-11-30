import spotipy, os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from utils import *

load_dotenv()
scope = "user-library-read,user-top-read,playlist-modify-private,playlist-read-private"

def print_matrix(matrix):
    for row in matrix:
        print("\t".join(str(x) for x in row))

def get_distance(track1, track2):
    mod_key = abs(track1["key"] - track2["key"])
    key_distance = min(mod_key, 12 - mod_key)
    mode_distance = abs(track1["mode"] - track2["mode"])
    if key_distance == 0 or (key_distance == 1 and mode_distance == 0):
        return 0
    return key_distance * (1 + mode_distance)

def create_distance_matrix(tracks):
    matrix = []
    for i in range(len(tracks)):
        row = []
        for j in range(i):
            row.append(get_distance(tracks[i], tracks[j]))
        matrix.append(row)
    return matrix

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               client_id=os.environ["CLIENT_ID"],
                                               client_secret=os.environ["CLIENT_SECRET"],
                                               redirect_uri=os.environ["REDIRECT_URI"]))

playlist_url = "https://open.spotify.com/playlist/3Eoo7f6WdG4OflyLfyhpGP?si=2e689a56ae574cf0"

playlist_id = get_playlist_id(playlist_url)

# Get all tracks from playlist
track_ids = [song["track"]["id"] for song in sp.playlist_tracks(playlist_id)["items"]]
tracks = sp.audio_features(track_ids)
print_matrix(create_distance_matrix(tracks))