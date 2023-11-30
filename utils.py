def get_playlist_id(playlist_url):
    return playlist_url.split("/")[-1].split("?")[0]