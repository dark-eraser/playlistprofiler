from utils.spotify_client import SpotipyClient
from utils.helper import *
from utils.visualization import *
import json
import argparse
def main():
    parser = argparse.ArgumentParser(description='Extract unique artists without genres from track files.')
    parser.add_argument('track_files', nargs='+', help='Path to track JSON files', default='data/tracks')
    args = parser.parse_args()
    
if __name__ == '__main__':
    main()