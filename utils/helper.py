import json

def get_artists_without_genres(tracks):
    """Extract unique artists without genres from track data."""
    artists_without_genres = {}
    for track in tracks:
        for artist in track['artists']:
            if not artist.get('genres'):
                artists_without_genres[artist['id']] = {
                    'id': artist['id'],
                    'name': artist['name']
                }
    return artists_without_genres

def get_all_unique_artists(tracks):
    """Extract all unique artists from track data."""
    return {
        artist["id"]: {"id": artist["id"], "name": artist["name"]}
        for track in tracks
        for artist in track["artists"]
    }
    
# Example usage:
    # parser = argparse.ArgumentParser(description='Extract unique artists without genres from track files.')
    # parser.add_argument('track_files', nargs='+', help='Path to track JSON files')
    # args = parser.parse_args()

    # unique_artists_without_genres, unique_artists = extract_artists_without_genres(args.track_files)
    # json.dumps(unique_artists_without_genres, indent=2)
    # print(len(unique_artists_without_genres), 'artists without genres found')
    # print(len(unique_artists), 'unique artists found')
    
def extract_artists_without_genres(track_files):
    """Main function to extract artists without genres and all unique artists."""
    unique_artists_without_genres = {}
    unique_artists = {}

    for file in track_files:
        tracks = load_file_data(file)
        unique_artists_without_genres.update(get_artists_without_genres(tracks))
        unique_artists.update(get_all_unique_artists(tracks))

    return list(unique_artists_without_genres.values()), unique_artists

def track_classifier(track_files):
    genre_groups = {}

    for file in track_files:
        data = load_file_data(file)
        process_tracks(data, genre_groups)

    return genre_groups


def load_file_data(file):
    with open(file, 'r') as f:
        return json.load(f)


def process_tracks(data, genre_groups):
    for track in data:
        track_genres = extract_track_genres(track)
        assign_genres_to_groups(track, track_genres, genre_groups)


def extract_track_genres(track):
    track_genres = set()
    for artist in track['artists']:
        if artist['genres']: 
            track_genres.update(artist['genres'])
    return track_genres


def assign_genres_to_groups(track, track_genres, genre_groups):
    """Assign tracks to genre groups."""
    if track_genres:
        for genre in track_genres:
            genre_groups.setdefault(genre, []).append(track['id'])
    else:
        genre_groups.setdefault('Unknown', []).append(track['id'])