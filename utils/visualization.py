import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from squarify import squarify

# Example usage:
# genre_groups = track_classifier(args.track_files)
# print(genre_groups)
# genre_distribution = {k: len(v) for k, v in genre_groups.items()}
# print(sorted(genre_distribution.items(), key=lambda x: -x[1]))
# genre_df, track_genre_matrix = prepare_genre_data(genre_groups)
# plot_genre_bars(genre_df, top_n=35)
# plot_genre_pie(genre_df, top_n=8)
# plot_genre_heatmap(track_genre_matrix)
# plot_genre_histogram(track_genre_matrix)
# plot_genre_treemap(genre_df)

def prepare_genre_data(genre_groups):
    """
    Prepare data structures for visualization
    Returns DataFrame and track-genre matrix
    """
    genre_df = pd.DataFrame.from_dict(
        {k: len(v) for k, v in genre_groups.items()}, 
        orient='index', 
        columns=['track_count']
    ).sort_values('track_count', ascending=False)
    
    track_genre_matrix = pd.DataFrame(
        [(track_id, genre) for genre, tracks in genre_groups.items() for track_id in tracks],
        columns=['track_id', 'genre']
    ).pivot_table(index='track_id', columns='genre', aggfunc=len, fill_value=0)
    
    return genre_df, track_genre_matrix

def plot_genre_bars(genre_df, top_n=20, figsize=(15,8)):
    """Bar plot of top genres"""
    plt.figure(figsize=figsize)
    sns.barplot(x=genre_df.index[:top_n], y=genre_df['track_count'][:top_n])
    plt.title(f'Top {top_n} Genres by Track Count')
    plt.xlabel('Genre')
    plt.ylabel('Number of Tracks')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_genre_pie(genre_df, top_n=10, figsize=(12,8)):
    """Pie chart of genre distribution"""
    top_genres = genre_df['track_count'][:top_n]
    others = genre_df['track_count'][top_n:].sum()
    
    sizes = list(top_genres) + [others]
    labels = list(top_genres.index) + ['Others']
    
    plt.figure(figsize=figsize)
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title(f'Genre Distribution (Top {top_n} + Others)')
    plt.axis('equal')
    plt.show()

def plot_genre_heatmap(track_genre_matrix, figsize=(12,10)):
    """Genre co-occurrence heatmap"""
    plt.figure(figsize=figsize)
    genre_correlation = track_genre_matrix.corr()
    sns.heatmap(genre_correlation, annot=False, cmap='YlGnBu')
    plt.title('Genre Co-occurrence Patterns')
    plt.tight_layout()
    plt.show()

def plot_genre_histogram(track_genre_matrix, figsize=(10,6)):
    """Distribution of genres per track"""
    genre_counts = track_genre_matrix.sum(axis=1)
    plt.figure(figsize=figsize)
    sns.histplot(genre_counts, kde=True, bins=range(1, genre_counts.max()+2))
    plt.title('Number of Genres per Track Distribution')
    plt.xlabel('Number of Genres')
    plt.ylabel('Number of Tracks')
    plt.show()

def plot_genre_treemap(genre_df, top_n=30, figsize=(16,10)):
    """Treemap visualization of genres"""
    plt.figure(figsize=figsize)
    squarify.plot(
        sizes=genre_df['track_count'][:top_n],
        label=genre_df.index[:top_n],
        alpha=.8,
        text_kwargs={'fontsize':10}
    )
    plt.title(f'Genre Popularity Treemap (Top {top_n})')
    plt.axis('off')
    plt.show()


