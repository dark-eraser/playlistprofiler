import json

def add_tracks_to_playlist(sp_client, tracks_files, playlist_id, genre="jazz"):
    """
    Add tracks to a Spotify playlist based on genre classification.
    Args:
        sp_client: Spotify client instance.
        tracks_files: List of JSON files containing track data.
        playlist_id: ID of the Spotify playlist to add tracks to.
        genre: Genre to filter tracks by (default is "jazz").
    """
    track_ids = []
    for file in tracks_files:
        try:
            with open(file, 'r') as file:
                tracks = json.load(file)
                for track in tracks:
                    artists = track.get("artists", [])
                    for artist in artists:
                        top_genres = artist.get("top_genres", [])
                        if any(genre.lower() == top_genre.lower() for top_genre in top_genres):
                            track_ids.append(track["id"])
        except Exception as e:
            print(f"Error processing file {file.name}: {e}")
    print(f"Found {len(track_ids)} tracks with genre {genre}")
    sp_client.playlist_add_items(playlist_id, track_ids)

def create_playlist(sp_client, playlist_name="Classified Playlist"):
    """Create a new playlist in the user's Spotify account."""
    user_id = sp_client.current_user()["id"]
    playlist = sp_client.user_playlist_create(
        user=user_id,
        name=playlist_name,
        public=False,
        description="Auto-generated playlist based on genre classification"
    )
    return playlist
