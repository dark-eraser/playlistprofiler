import json
import os

# Define the input file path
input_file = '../data/last_saved_tracks.json'

# Define the output directory
output_dir = '../data/tracks'
os.makedirs(output_dir, exist_ok=True)

# Number of tracks per file
tracks_per_file = 500

# Read the entire JSON file
with open(input_file, 'r') as f:
    data = json.load(f)

# Split the data into chunks of 500 tracks
for i in range(0, len(data), tracks_per_file):
    chunk = data[i:i + tracks_per_file]
    
    # Create a new file for each chunk
    output_file = os.path.join(output_dir, f'tracks_{i//tracks_per_file + 1}.json')
    with open(output_file, 'w') as f:
        json.dump(chunk, f, indent=4)

print(f"Split {len(data)} tracks into {len(data) // tracks_per_file + (1 if len(data) % tracks_per_file != 0 else 0)} files.")
