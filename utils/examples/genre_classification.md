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