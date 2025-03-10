import json
import os
import time
import random
from tqdm import tqdm
from spotify_client import SpotipyClient
from requests.exceptions import ConnectionError
import logging
import pickle
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("spotify_api.log"),
        logging.StreamHandler()
    ]
)

# Cache for artist details to avoid redundant API calls
CACHE_FILE = "artist_cache.pkl"
PROGRESS_FILE = "progress.json"

def load_cache():
    """Load the artist cache if it exists"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            logging.warning(f"Failed to load cache: {e}")
    return {}

def save_cache(cache):
    """Save the artist cache to disk"""
    try:
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump(cache, f)
    except Exception as e:
        logging.warning(f"Failed to save cache: {e}")

def save_progress(file_path, processed_indices):
    """Save the current progress to allow resuming"""
    try:
        with open(PROGRESS_FILE, 'w') as f:
            json.dump({
                'file_path': file_path,
                'processed_indices': list(processed_indices),
                'timestamp': datetime.now().isoformat()
            }, f)
    except Exception as e:
        logging.warning(f"Failed to save progress: {e}")

def load_progress(file_path):
    """Load the progress file if it exists and matches the current file"""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                progress = json.load(f)
                if progress['file_path'] == file_path:
                    return set(progress['processed_indices'])
        except Exception as e:
            logging.warning(f"Failed to load progress: {e}")
    return set()

# Function to get artist details
def get_artist_details(sp, artist_id):
    # Check cache first
    artist_cache = load_cache()
    if artist_id in artist_cache:
        logging.info(f"Using cached data for artist {artist_id}")
        return artist_cache[artist_id]

    max_retries = 5
    base_delay = 1
    for attempt in range(max_retries):
        try:
            result = sp.artist(artist_id)
            # Cache the result
            artist_cache[artist_id] = result
            save_cache(artist_cache)
            return result
        except ConnectionError as e:
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            logging.warning(f"Connection error for artist {artist_id}. Retrying in {delay:.2f} seconds... (Attempt {attempt+1}/{max_retries})")
            time.sleep(delay)
        except Exception as e:
            # Check if it's a rate limit error
            if "429" in str(e):
                retry_after = int(getattr(e, 'headers', {}).get('Retry-After', 30))
                logging.warning(f"Rate limit hit, waiting for {retry_after} seconds before retrying...")
                time.sleep(retry_after)
                continue
            if attempt == max_retries - 1:
                logging.error(f"Failed to fetch artist details for {artist_id} after {max_retries} attempts: {e}")
                return None
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            logging.warning(f"Error for artist {artist_id}: {e}. Retrying in {delay:.2f} seconds...")
            time.sleep(delay)
    return None

# Main function to update tracks with artist details
def update_tracks_with_artist_details(file_path):
    # Load credentials from creds.json
    try:
        with open('creds.json', 'r') as f:
            creds = json.load(f)
            client_id = creds.get('client_id', '')
            client_secret = creds.get('client_secret', '')
            redirect_uri = creds.get('redirect_uri', 'http://localhost:8080')
            scope = creds.get('scope', '')
    except Exception as e:
        logging.error(f"Error loading credentials: {e}")
        sys.exit(1)
    
    sp = SpotipyClient(client_id, client_secret, redirect_uri, scope).get_token()
    logging.info(f"Starting to update tracks from {file_path}")

    # Load processed track indices to resume if needed
    processed_indices = load_progress(file_path)
    if processed_indices:
        logging.info(f"Resuming from previous run, already processed {len(processed_indices)} tracks")

    with open(file_path, 'r') as f:
        tracks = json.load(f)

    total_tracks = len(tracks)
    logging.info(f"Found {total_tracks} tracks to process")
    
    # Use tqdm for progress reporting
    for idx, track_entry in enumerate(tqdm(tracks, desc="Updating tracks", unit="track")):
        # Skip already processed tracks
        if idx in processed_indices:
            continue
        for artist in track_entry['artists']:
            artist_id = artist['id']
            artist_details = get_artist_details(sp, artist_id)
            if artist_details:
                artist.update(artist_details)
            
            # Add a delay to avoid hitting rate limits
            delay = random.uniform(1, 2)  # Increased delay to be more conservative
            time.sleep(delay)
        
        # Mark this track as processed
        processed_indices.add(idx)
        
        # Save progress periodically (every 10 tracks)
        if idx % 10 == 0:
            save_progress(file_path, processed_indices)
            # Also save the current state of the tracks
            with open(f"{file_path}.partial", 'w') as f:
                json.dump(tracks, f, indent=4)
    
    # Write the updated tracks back to the file
    with open(file_path, 'w') as f:
        json.dump(tracks, f, indent=4)
    
    # Clear progress file as we've completed successfully
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
    
    logging.info(f"Successfully updated all {total_tracks} tracks")

# Example usage:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = '../data/tracks/tracks_2.json'
        
    logging.info(f"Starting processing of {file_path}")
    update_tracks_with_artist_details(file_path)
    logging.info("Processing completed")
