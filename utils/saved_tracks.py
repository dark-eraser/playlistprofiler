import json
import os
from spotify_client import SpotipyClient
import time
import random
from requests.exceptions import ConnectionError
from http.client import RemoteDisconnected

def get_last_saved_tracks(sp, limit=100):
    file_path = '../data/temp_saved_tracks.json'
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                saved_track_ids = json.load(f)
                if len(saved_track_ids) > 0:
                    print(f"Reading {limit} tracks from the saved file...")
                    tracks = [{'track_id': track_id} for track_id in saved_track_ids[:limit]]
                    return tracks
                else:
                    print(f"File exists but contains no saved tracks.")
            except json.JSONDecodeError:
                print(f"File exists but contains invalid JSON. Fetching tracks from Spotify.")
    
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
        delay = random.uniform(0.5, 1)
        time.sleep(delay)
    print(f"Finished fetching {len(tracks)} tracks.")
    
    with open(file_path, 'w') as f:
        json.dump([track['track']['id'] for track in tracks], f, indent=4)
    
    return tracks[:limit]

def save_tracks_to_json(tracks, sp, file_path='../data/last_saved_tracks.json'):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                existing_tracks = json.load(f)
            except json.JSONDecodeError:
                print(f"File exists but contains invalid JSON. Starting with an empty list.")
                existing_tracks = []
    else:
        existing_tracks = []

    existing_track_ids = set(track['id'] for track in existing_tracks)

    # Check for the last gathered track ID
    if existing_tracks:
        last_gathered_track_id = existing_tracks[-1]['id']
        print(f"Last gathered track ID: {last_gathered_track_id}")
        start_index = next((i for i, track in enumerate(tracks) if track['track_id'] == last_gathered_track_id), None)
        if start_index is not None:
            tracks = tracks[start_index + 1:]  # Start from the next track after the last gathered one
        else:
            print("Last gathered track not found in the current list. Starting from the beginning.")
    else:
        print("No previous tracks found. Starting from the beginning.")

    with open(file_path, 'a') as f:
        if existing_tracks:
            f.write(',\n')  # Add a comma and newline to separate from the previous JSON array

        total_tracks = len(tracks)
        print(f"Processing {total_tracks} tracks...")
        
        for i, track in enumerate(tracks, 1):
            track_id = track['track_id']
            if track_id not in existing_track_ids:
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        detailed_track = sp.track(track_id)
                        break
                    except (ConnectionError, RemoteDisconnected) as e:
                        if attempt == max_retries - 1:
                            print(f"Failed to fetch track {track_id} after {max_retries} attempts: {e}")
                            continue
                        print(f"Connection error for track {track_id}. Retrying in {attempt + 1} seconds...")
                        time.sleep(attempt + 1)
                
                if 'detailed_track' not in locals():
                    print(f"Skipping track {track_id} due to persistent connection issues.")
                    continue
                
                track_data = {
                    'id': detailed_track['id'],
                    'name': detailed_track['name'],
                    'artists': [{'id': artist['id'], 'name': artist['name']} for artist in detailed_track['artists']],
                    'album': {
                        'id': detailed_track['album']['id'],
                        'name': detailed_track['album']['name'],
                        'release_date': detailed_track['album']['release_date'],
                        'total_tracks': detailed_track['album']['total_tracks'],
                        'images': detailed_track['album']['images']
                    },
                    'duration_ms': detailed_track['duration_ms'],
                    'explicit': detailed_track['explicit'],
                    'popularity': detailed_track.get('popularity', None),
                    'preview_url': detailed_track.get('preview_url', None),
                    'available_markets': detailed_track['available_markets']
                }

                json.dump(track_data, f, indent=4)
                if i < total_tracks:  # Add a comma after each track except the last one
                    f.write(',\n')
                existing_tracks.append(track_data)
                
                if i % 10 == 0 or i == total_tracks: 
                    print(f"Processed {i}/{total_tracks} tracks.")
            else:
                print(f"Skipping track {track_id} as it's already in the file.")
            
            delay = random.uniform(0.5, 1)
            time.sleep(delay)


# Example usage:
if __name__ == '__main__':
    spotipyclient = SpotipyClient('SpotipyClientname', 'password', 'http://localhost:8080', '')
    sp = spotipyclient.get_token()
    last_saved_tracks = get_last_saved_tracks(sp, limit=5000)
    save_tracks_to_json(last_saved_tracks, sp)
