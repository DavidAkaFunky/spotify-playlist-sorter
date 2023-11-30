import spotipy, os
from dotenv import load_dotenv
from utils import *
from random import randint
from numpy import argmin

load_dotenv()
scope = "user-library-read,user-top-read,playlist-modify-private,playlist-read-private"

sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(scope=scope,
                                                              client_id=os.environ["CLIENT_ID"],
                                                              client_secret=os.environ["CLIENT_SECRET"],
                                                              redirect_uri=os.environ["REDIRECT_URI"]))

MAX_INT = 100000

def get_camelot_distance(track1, track2):
    """Returns the distance between two tracks in the Camelot wheel"""
    if track1["key"] == track2["key"] and track1["mode"] == track2["mode"]:
        return 0
    
    camelot_key1, camelot_key2 = get_camelot(track1["key"], track1["mode"])[0], get_camelot(track2["key"], track2["mode"])[0]
    mod_key = abs(camelot_key1 - camelot_key2)
    
    key_distance = min(mod_key, 12 - mod_key) / 6 # 6 is the max distance between two keys, scale to [0, 1]
    mode_distance = abs(track1["mode"] - track2["mode"])
    
    return (key_distance * (1 + mode_distance)) / (1 * 2) # 2 is the max distance between two tracks, scale to [0, 1]

def get_bpm_distance(track1, track2):
    return abs(track1["tempo"] - track2["tempo"]) / 40 # Compare a 40 bpm difference to a 1 distance

def get_distance(track1, track2):
    if track1["tempo"] == track2["tempo"] and track1["key"] == track2["key"] \
        and track1["time_signature"] == track2["time_signature"] and track1["mode"] == track2["mode"]:
        return MAX_INT # They are the same track but with different IDs
    
    return get_camelot_distance(track1, track2) * 0.7 + get_bpm_distance(track1, track2) * 0.3

def create_distance_matrix(tracks):
    matrix = []
    for i in range(len(tracks)):
        row = []
        for j in range(len(tracks)):
            if i == j:
                row.append(MAX_INT)
            else:
                row.append(get_distance(tracks[i], tracks[j]))
        matrix.append(row)
    return matrix

def create_track_order(tracks, distance_matrix):
    was_chosen = {i: False for i in range(len(tracks))}
    order = [randint(0, len(tracks) - 1)]
    for _ in range(len(tracks) - 1):
        choice = order[-1]
        was_chosen[choice] = True
        distance_list = [distance_matrix[choice][j] if not was_chosen[j] else MAX_INT for j in range(len(tracks))]
        min_index = argmin(distance_list)
        order.append(min_index)
    return order

def order_tracks(tracks, order, tracks_features=None):
    if tracks_features is None:
        return [tracks[i] for i in order], None
    return [tracks[i] for i in order], [tracks_features[i] for i in order]

def get_playlist_tracks(playlist_id):
    """Returns a list of all tracks in a playlist
       This is required because Spotify's API only returns 100 tracks at a time"""
    tracks = []
    offset = 0
    while True:
        response = sp.playlist_tracks(playlist_id, offset=offset)
        tracks.extend(response["items"])
        if response["next"] is None:
            break
        offset += 100
    return tracks

def get_playlist_audio_features(track_ids):
    tracks_features = []
    offset = 0
    while True:
        response = sp.audio_features(track_ids[offset:offset + 100])
        tracks_features.extend(response)
        if len(response) < 100:
            break
        offset += 100
    return tracks_features

def print_playlist_tracks(tracks, tracks_features=None):
    for i, track in enumerate(tracks):
        if tracks_features is None:
            print(f"{i + 1}. {get_track_name_and_artist(track)}")
        else:
            print(f"{i + 1}. {get_track_name_and_artist(track, tracks_features[i])}")

def filter_duplicate_tracks(tracks):
    """Filters out duplicate tracks from a list of tracks"""
    track_ids = {}
    for track in tracks:
        track_id = track["track"]["id"]
        try:
            track_ids[track_id] = track
        except KeyError:
            pass
    return list(track_ids.keys()), list(track_ids.values())

def create_sorted_playlist(playlist, test=False):
    playlist_id = get_playlist_id(playlist)
    tracks = get_playlist_tracks(playlist_id)
    if test:
        tracks = tracks[:10]
    track_ids, tracks = filter_duplicate_tracks(tracks)
    tracks_features = get_playlist_audio_features(track_ids)
    distance_matrix = create_distance_matrix(tracks_features)
    track_order = create_track_order(tracks_features, distance_matrix)
    tracks, tracks_features = order_tracks(tracks, track_order, tracks_features=tracks_features)
    print_playlist_tracks(tracks, tracks_features=tracks_features)
        
    # Might be useful if you want to change the original playlist
    #sp.user_playlist_replace_tracks(sp.me()["id"], playlist_id, sorted_track_ids)