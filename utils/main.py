# from utils.spotify_client import SpotipyClient
from helper import *
from visualization import *
from genre_classification import classify_subgenre
import json
import argparse
def main():
    parser = argparse.ArgumentParser(description='Extract unique artists without genres from track files.')
    parser.add_argument('track_files', nargs='+', help='Path to track JSON files', default='data/tracks')
    args = parser.parse_args()
    with open ('/Users/darkeraser/Documents/dev/playlistprofiler/data/genres.json', 'r') as f:
        genres = json.load(f)
        for file_path in args.track_files:
            with open(file_path, 'r') as f:
                tracks = json.load(f)
                for track in tracks:
                    for artist in track['artists']:
                        artist_subgenres = artist.get('genres', [])
                        for subgenre in artist_subgenres:
                            top_genre = classify_subgenre(subgenre, genres)
                            artist['top_genre'] = top_genre
    with open(file_path, 'w') as f:
        json.dump(tracks, f, indent=4)
    print(f"Processed {len(tracks)} tracks from {file_path}")
    
if __name__ == '__main__':
    main()