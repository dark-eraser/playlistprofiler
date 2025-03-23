from utils.spotify_client import SpotipyClient
from utils.helper import *
from utils.visualization import *
import json
import argparse
def main():
    parser = argparse.ArgumentParser(description='Extract unique artists without genres from track files.')
    parser.add_argument('track_files', nargs='+', help='Path to track JSON files')
    args = parser.parse_args()
    genre_groups = track_classifier(args.track_files)
    # print(genre_groups)
    genre_distribution = {k: len(v) for k, v in genre_groups.items()}
    # print(sorted(genre_distribution.items(), key=lambda x: -x[1]))
    genre_df, track_genre_matrix = prepare_genre_data(genre_groups)
    plot_genre_bars(genre_df, top_n=35)
    # plot_genre_pie(genre_df, top_n=8)
    # plot_genre_heatmap(track_genre_matrix)
    # plot_genre_histogram(track_genre_matrix)
    # plot_genre_treemap(genre_df)
    
if __name__ == '__main__':
    main()