def get_playlist_id(playlist_url):
    return playlist_url.split("/")[-1].split("?")[0]

def get_camelot(key, mode):
    """Keys are initially s.t. C -> 0, C# -> 1, D -> 2, ..., B -> 11
       Modes are s.t. Minor -> 0, Major -> 1
       However, in the Camelot wheel:
       C Major -> 8B, C# Major -> 3B, D Major -> 10B, ..., B Major -> 5B
       C Minor is 5A, C# Minor is 12A, D Minor is 7A, ..., B Minor is 2A"""
    return (5 + 3 * mode + 7 * key) % 12 + 1, "A" if mode == 0 else "B"

def get_track_name_and_artist(track, track_features=None):
    track_info = track["track"]
    name = track_info["name"]
    artists = ", ".join(artist["name"] for artist in track_info["artists"])
    if track_features is None:
        return f"{name} by {artists}"
    bpm = track_features["tempo"]
    camelot = "".join(str(x) for x in get_camelot(track_features["key"], track_features["mode"]))
    return f"{name} - {artists} - {bpm} BPM - Camelot Key: {camelot}"

def print_matrix(matrix):
    for row in matrix:
        print("\t".join(str(x) for x in row))