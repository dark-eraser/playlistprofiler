## Track-Genre Classification
Given a json file of sub genres and their association to top-level genres, classify track files based on the subgenres the artists of the given tracks are associated with:

```python
parser = argparse.ArgumentParser(description='Extract unique artists without genres from track files.')
parser.add_argument('track_files', nargs='+', help='Path to track JSON files', default='data/tracks')
args = parser.parse_args()

with open ('genres.json', 'r') as f:
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
```

## Utility for Genre Classification

This script processes JSON files containing track and artist data, classifies each artist's subgenres into top-level genres, and updates the JSON files accordingly. It uses a genres.json file to validate and map subgenres to predefined top-level genres. The script also clears any existing top_genre field and replaces it with a new top_genres field containing validated classifications.

```python
    with open('genres.json', 'r') as f:
        genre_data = json.load(f)
        valid_genres = list(genre_data.keys())

    for file_path in args.track_files:
        with open(file_path, 'r') as f:
            tracks = json.load(f)
        for track in tracks:
            for artist in track['artists']:
                artist.pop('top_genres', None)
                artist_subgenres = artist.get('genres', [])
                top_genres = []
                for subgenre in artist_subgenres:
                    top_genre = classify_subgenre(subgenre, valid_genres)
                    if top_genre and top_genre in valid_genres and top_genre not in top_genres:
                        top_genres.append(top_genre)
                if top_genres:
                    artist['top_genres'] = top_genres

        with open(file_path, 'w') as f:
            json.dump(tracks, f, indent=4)

```