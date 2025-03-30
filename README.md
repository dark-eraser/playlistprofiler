# PlaylistProfiler


## Description

Playlistprofiler is a tool to help you organize your liked songs into playlists based on their genre and mood at its core, but can also do so much more, like:

- provide cool visualization for your spotify data
- provide insights in your most listened-to genres

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/playlistprofiler.git
   ```
2. Navigate to the project directory:
   ```bash
   cd playlistprofiler
   ```
3. Install the required dependencies:
   ```bash
   pipenv install
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. Follow the prompts to define playlists based on your preferences.

## File Structure

```
playlistprofiler/
├── main.py                      # Entry point of the application
├── requirements.txt             # List of dependencies
├── README.md                    # Project documentation
├── spotify_genres.json          # list of available spotify genres
├── data/                        # Directory for storing data files
├── examples/                    # Example use cases of the different functions to get started
├── utils/                       # Utility functions and helpers
│   ├── spotify_client.py        # Spotify API client for authentication and requests
│   ├── saved_tracks.py          # Functions to fetch and save Spotify tracks
│   ├── helper.py                # Helper functions for processing track and artist data
│   └── genres.py                # Functions to classify tracks by genre and update artist details
│   ├── visualization.py         # A few functions to help visualize your spotify data
│   ├── playlist.py              # Function to interact with playlist objects
│   ├── file_splitting.py         # For better performance
│   └── genre_classification.py   # Functions to organize subgenres into top-level genres, with
                                 # different classification methods
```

## Contents of Codebase processing data.

- **main.py**: The main script to run the application.
- **data/**: Directory for storing input and output data files.
- **utils/**: Contains helper functions and utility scripts for processing data:Contributions are welcome! Please follow these steps:
  - **spotify_client.py**: Spotify API client for authentication and requests.
  - **saved_tracks.py**: Functions to fetch and save Spotify tracks.
  - **helper.py**: Helper functions for processing track and artist data
  - **genres.py**: Functions to classify tracks by genre and update artist details.

## Contributing## License

Contributions are welcome! Please follow these steps:This project is licensed under the MIT License.

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push the branch.
4. Submit a pull request.

## License

This project is licensed under the MIT License.

## References
- Spotify Genre List: https://gist.github.com/andytlr/4104c667a62d8145aa3a 
    - last update 10 years ago but there is no more recent record of these and the API endpoint has been discontinued:
    https://developer.spotify.com/documentation/web-api/reference/get-recommendation-genres