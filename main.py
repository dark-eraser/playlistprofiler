from utils.spotify_client import SpotipyClient

if __name__ == '__main__':
    spotipyclient = SpotipyClient('SpotipyClientname', 'password', 'http://localhost:8080', '')
    creds = spotipyclient.load_credentials()
    sp = spotipyclient.get_token()
    last_saved_tracks = spotipyclient.get_last_saved_tracks(sp, limit=5000)
    spotipyclient.save_tracks_to_json(last_saved_tracks)
    # for track in last_saved_tracks:
    #     print(track['track']['name'])
