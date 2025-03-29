import json
import re
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load subgenres and top-level genres
with open('subgenres.json', 'r') as f:
    subgenres = json.load(f)

top_level_genres = [
    "Rock", "Pop", "Hip Hop", "Electronic", "Jazz", "Classical", "R&B/Soul",
    "Country", "Folk", "Metal", "Blues", "Reggae", "Latin", "World Music",
    "Punk", "Funk", "Gospel", "Indie", "Alternative", "Experimental"
]

def preprocess(genre):
    return re.sub(r'[^\w\s]', '', genre.lower())

def rule_based_matching(subgenre, top_genres):
    # Check if subgenre is a string
    if not isinstance(subgenre, str):
        return None
        
    subgenre_lower = subgenre.lower()
    
    # Handle dictionary structure
    if isinstance(top_genres, dict):
        genre_names = list(top_genres.keys())
    else:
        genre_names = top_genres
        
    for genre in genre_names:
        if genre.lower() in subgenre_lower:
            return genre
    return None

def fuzzy_matching(subgenre, top_genres, threshold=80):
    # Check if subgenre is a string
    if not isinstance(subgenre, str):
        return None
        
    max_score = 0
    best_match = None
    
    # Handle dictionary structure
    if isinstance(top_genres, dict):
        genre_names = list(top_genres.keys())
    else:
        genre_names = top_genres
        
    for genre in genre_names:
        score = fuzz.ratio(subgenre.lower(), genre.lower())
        if score > max_score and score >= threshold:
            max_score = score
            best_match = genre
    return best_match

def semantic_similarity(subgenre, top_genres):
    # Check if subgenre is a string
    if not isinstance(subgenre, str):
        return None
        
    # Handle dictionary structure
    if isinstance(top_genres, dict):
        genre_names = list(top_genres.keys())
    else:
        genre_names = top_genres
        
    all_genres = [subgenre] + genre_names
    tfidf = TfidfVectorizer().fit_transform([preprocess(g) for g in all_genres])
    similarities = cosine_similarity(tfidf[0:1], tfidf[1:])[0]
    return genre_names[similarities.argmax()] if similarities.max() > 0.1 else None

def classify_subgenre(subgenre, top_genres):
    # Handle empty input
    if not subgenre:
        return "Other"
        
    # Handle list of subgenres
    if isinstance(subgenre, list):
        if not subgenre:  # Empty list
            return "Other"
            
        # Process each subgenre and collect the results
        results = []
        for single_subgenre in subgenre:
            if single_subgenre:  # Skip empty strings
                result = classify_single_subgenre(single_subgenre, top_genres)
                if result:
                    results.append(result)
                    
        if not results:  # No valid results
            return "Other"
            
        # Count occurrences of each genre and return the most common
        genre_counts = {}
        for genre in results:
            genre_counts[genre] = genre_counts.get(genre, 0) + 1
            
        # Get the most frequent genre
        return max(genre_counts.items(), key=lambda x: x[1])[0]
    else:
        # Handle single string subgenre
        return classify_single_subgenre(subgenre, top_genres)

def classify_single_subgenre(subgenre, top_genres):
    # Rule-based matching
    match = rule_based_matching(subgenre, top_genres)
    if match:
        return match

    # Fuzzy matching
    match = fuzzy_matching(subgenre, top_genres)
    if match:
        return match

    # Semantic similarity
    match = semantic_similarity(subgenre, top_genres)
    if match:
        return match

    return "Other"

# Classify all subgenres
classification = {}
for subgenre in subgenres:
    top_genre = classify_subgenre(subgenre, top_level_genres)
    if top_genre not in classification:
        classification[top_genre] = []              
    classification[top_genre].append(subgenre)

with open('genres.json', 'w') as f:  
    json.dump(classification, f, indent=4)

        