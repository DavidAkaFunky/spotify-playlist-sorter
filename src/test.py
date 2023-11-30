from spotify import *

playlist_url = "https://open.spotify.com/playlist/6NbZNkZAszmkOInS7Qs06y?si=8a6e8f0ea05d4d3e"

# Get all tracks from playlist
create_sorted_playlist(playlist_url)

# tracks = sp.audio_features(track_ids)
#print_matrix(create_distance_matrix(tracks))