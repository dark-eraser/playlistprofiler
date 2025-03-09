import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotipyClient:
    def __init__(self, username, client_secret, redirect_uri, scope):
        self.username = username
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope

    @staticmethod
    def load_credentials(file_path='creds.json'):
        """Loads credentials from a JSON file."""
        try:
            with open(file_path) as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return None

    def get_token(self):
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=creds['client_id'],
                                                       client_secret=creds['client_secret'],
                                                       redirect_uri=creds['redirect_uri'],
                                                       scope=creds['scope']))
        return sp