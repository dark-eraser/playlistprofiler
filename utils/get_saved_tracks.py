import json
import os
from utils.spotify_client import SpotipyClient
import time
import random


def get_playlists(self):
    sp = self.get_token()
    playlists = sp.current_user_playlists()  # Corrected method name
    return playlists

def get_last_saved_tracks(self, sp, limit=100):
    tracks = []
    offset = 0
    print(f"Fetching saved tracks up to {limit}...")
    while len(tracks) < limit:
        results = sp.current_user_saved_tracks(limit=20, offset=offset)
        tracks.extend(results['items'])
        if not results['next']:
            break
        offset += 20
        print(f"Fetched {len(tracks)} tracks so far...")
        delay = random.uniform(0.5, 2)
        time.sleep(delay)
    print(f"Finished fetching {len(tracks)} tracks.")
    return tracks[:limit]

def save_tracks_to_json(self, tracks, file_path='data/last_saved_tracks.json'):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    track_data = [{'name': track['track']['name'], 'id': track['track']['id']} for track in tracks]
    with open(file_path, 'w') as f:
        json.dump(track_data, f, indent=4)
    print(f"Tracks saved to {file_path}.")

def get_artist_genres(self, sp, artist_id):
    try:
        artist = sp.artist(artist_id)
        return artist.get('genres', [])  # Use get() to avoid KeyError
    except Exception as e:
        print(f"Failed to get genres for artist {artist_id}: {e}")
        return []

def get_track_artist_genres(self, sp, track_id):
    try:
        track = sp.track(track_id)
        artist_ids = [artist['id'] for artist in track['artists']]
        genres = []
        for artist_id in artist_ids:
            artist_genres = self.get_artist_genres(sp, artist_id)
            if artist_genres:
                genres.extend(artist_genres)
        return list(set(genres))  # Remove duplicates
    except Exception as e:
        print(f"Failed to get genres for track {track_id}: {e}")
        return []
        
# Example usage:
# if __name__ == '__main__':
#     spotipyclient = SpotipyClient('SpotipyClientname', 'password', 'http://localhost:8080', '')
#     creds = spotipyclient.load_credentials()
#     sp = spotipyclient.get_token()
#     last_saved_tracks = spotipyclient.get_last_saved_tracks(sp, limit=5000)
#     spotipyclient.save_tracks_to_json(last_saved_tracks)
