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
    subgenre_lower = subgenre.lower()
    for genre in top_genres:
        if genre.lower() in subgenre_lower:
            return genre
    return None

def fuzzy_matching(subgenre, top_genres, threshold=80):
    max_score = 0
    best_match = None
    for genre in top_genres:
        score = fuzz.ratio(subgenre.lower(), genre.lower())
        if score > max_score and score >= threshold:
            max_score = score
            best_match = genre
    return best_match

def semantic_similarity(subgenre, top_genres):
    all_genres = [subgenre] + top_genres
    tfidf = TfidfVectorizer().fit_transform([preprocess(g) for g in all_genres])
    similarities = cosine_similarity(tfidf[0:1], tfidf[1:])[0]
    return top_genres[similarities.argmax()] if similarities.max() > 0.1 else None

def classify_subgenre(subgenre, top_genres):
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

# Print results
for genre, sub_genres in classification.items():
    print(f"{genre}: {len(sub_genres)} subgenres")
    print(", ".join(sub_genres[:5]) + ("..." if len(sub_genres) > 5 else ""))
    print()
