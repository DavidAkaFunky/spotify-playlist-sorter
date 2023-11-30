from spotify import *

playlist_url = "https://open.spotify.com/playlist/0clDclCh9VXifrLf4iqzEy?si=DijqxyMNTwmc15bFs1dOnQ"

# Get all tracks from playlist
create_sorted_playlist(playlist_url)

# tracks = sp.audio_features(track_ids)
#print_matrix(create_distance_matrix(tracks))