import json
import argparse
from playlist import *
from spotify_client import SpotipyClient

def main():
    parser = argparse.ArgumentParser(description='Extract unique artists without genres from track files.')
    parser.add_argument('track_files', nargs='+', help='Path to track JSON files', default='data/tracks')
    args = parser.parse_args()
    spotipyclient = SpotipyClient('SpotipyClientname', 'password', 'http://localhost:8080', '')
    sp = spotipyclient.get_token()
    playlist = create_playlist(sp, playlist_name="Jazzy")
    add_tracks_to_playlist(sp, args.track_files, playlist_id=playlist['id'], genre="jazz")
    
if __name__ == '__main__':
    main()
