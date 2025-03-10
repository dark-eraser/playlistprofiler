import json
import os
import time
import random
from tqdm import tqdm
from spotify_client import SpotipyClient
from requests.exceptions import ConnectionError

# Function to get artist details
def get_artist_details(sp, artist_id):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return sp.artist(artist_id)
        except (ConnectionError) as e:
            if attempt == max_retries - 1:
                print(f"Failed to fetch artist details for {artist_id} after {max_retries} attempts: {e}")
                return None
            print(f"Connection error for artist {artist_id}. Retrying in {attempt + 1} seconds...")
            time.sleep(attempt + 1)
    return None

# Main function to update tracks with artist details
def update_tracks_with_artist_details(file_path):
    sp = SpotipyClient('SpotipyClientname', '', 'http://localhost:8080', '').get_token()
    
    with open(file_path, 'r') as f:
        tracks = json.load(f)
    
    # Use tqdm for progress reporting
    for track_entry in tqdm(tracks, desc="Updating tracks", unit="track"):
        for artist in track_entry['artists']:
            artist_id = artist['id']
            artist_details = get_artist_details(sp, artist_id)
            if artist_details:
                artist.update(artist_details)
            
            # Add a delay to avoid hitting rate limits
            delay = random.uniform(0.5, 1)
            time.sleep(delay)
    
    # Write the updated tracks back to the file
    with open(file_path, 'w') as f:
        json.dump(tracks, f, indent=4)

# Example usage:
if __name__ == '__main__':
    file_path = '../data/tracks/tracks_1.json'
    update_tracks_with_artist_details(file_path)
