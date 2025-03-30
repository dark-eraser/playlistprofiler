## Track-Genre Classification
Create new Spotify playlist and add tracks to it depending on their genre (jazz example here).

Source file: `playlist.py`
```python
    spotipyclient = SpotipyClient('SpotipyClientname', 'password', 'http://localhost:8080', '')
    sp = spotipyclient.get_token()
    playlist = create_playlist(sp, playlist_name="Jazzy")
    add_tracks_to_playlist(sp, args.track_files, playlist_id=playlist['id'], genre="jazz")
```
