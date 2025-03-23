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
├── main.py               # Entry point of the application
├── requirements.txt      # List of dependencies
├── README.md             # Project documentation
├── data/                 # Directory for storing data files
├── utils/                # Utility functions and helpers
│   ├── spotify_client.py # Spotify API client for authentication and requests
│   ├── saved_tracks.py   # Functions to fetch and save Spotify tracks
│   ├── helper.py         # Helper functions for processing track and artist data
│   └── genres.py         # Functions to classify tracks by genre and update artist details
└── tests/                # Unit tests for the application
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
