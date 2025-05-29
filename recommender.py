import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack, csr_matrix
from collections import Counter

# Load and clean data
df = pd.read_csv("dataset.csv")
df = df.dropna()
df = df.drop_duplicates()
if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

track_index = {name.lower(): i for i, name in enumerate(df['track_name'])}

numerical_features = [
    'danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
    'instrumentalness', 'liveness', 'valence', 'tempo', 'popularity', 'duration_ms'
]

scaler = MinMaxScaler()
df['valence'] *= 1.5
df['energy'] *= 1.2
df['popularity'] *= 1.2
num_scaled = scaler.fit_transform(df[numerical_features])

artist_tfidf = TfidfVectorizer()
artist_vecs = artist_tfidf.fit_transform(df['artists'])

genre_tfidf = TfidfVectorizer()
genre_vecs = genre_tfidf.fit_transform(df['track_genre'])

title_tfidf = TfidfVectorizer()
title_vecs = title_tfidf.fit_transform(df['track_name'])

album_tfidf = TfidfVectorizer()
album_vecs = album_tfidf.fit_transform(df['album_name'])

final_song_vectors = hstack([csr_matrix(num_scaled), genre_vecs, artist_vecs, title_vecs, album_vecs])

model = NearestNeighbors(metric='cosine')
model.fit(final_song_vectors)

kmeans = KMeans(n_clusters=20, random_state=42)
clusters = kmeans.fit_predict(final_song_vectors)

def recommend_songs_cluster(liked_songs, top_n=10, max_k_j=2, show_matches=True):
    matched = []
    unmatched = []
    liked_indices = []
    for name in liked_songs:
        name_lower = name.lower()
        if name_lower in track_index:
            liked_indices.append(track_index[name_lower])
            matched.append(name)
        else:
            unmatched.append(name)

    if show_matches:
        print("Matched:", matched)
        print("Not found:", unmatched)

    if not liked_indices:
        return "No liked songs found in dataset."

    k_j_genres = ['k-pop', 'j-pop', 'j-rock', 'j-dance', 'j-idol']
    liked_k_j_count = 0
    for idx in liked_indices:
        genre = str(df.iloc[idx]['track_genre']).lower().strip()
        if genre in k_j_genres:
            liked_k_j_count += 1

    if liked_k_j_count >= 5:
        k_j_limit = top_n
        print(f"User likes {liked_k_j_count} K/J songs - no genre limit applied")
    else:
        k_j_limit = max_k_j
        print(f"User likes {liked_k_j_count} K/J songs - limiting to {k_j_limit} K/J recommendations")

    liked_clusters = clusters[liked_indices]
    cluster_counts = Counter(liked_clusters)
    target_cluster = cluster_counts.most_common(1)[0][0]
    cluster_songs = np.where(clusters == target_cluster)[0]

    cluster_vectors = final_song_vectors[cluster_songs]
    liked_vectors = final_song_vectors[liked_indices]
    user_profile = np.asarray(liked_vectors.mean(axis=0))
    similarities = cosine_similarity(user_profile, cluster_vectors).flatten()
    ranked_cluster_indices = similarities.argsort()[::-1]

    seen_names = set()
    recommended_indices = []
    k_j_count = 0

    for idx in ranked_cluster_indices:
        actual_idx = cluster_songs[idx]
        name = df.iloc[actual_idx]['track_name']
        genre = str(df.iloc[actual_idx]['track_genre']).lower().strip()

        if actual_idx in liked_indices or name in seen_names:
            continue

        is_k_j = genre in k_j_genres
        if is_k_j and k_j_count >= k_j_limit:
            continue

        seen_names.add(name)
        recommended_indices.append(actual_idx)
        if is_k_j:
            k_j_count += 1
        if len(recommended_indices) == top_n:
            break

    result_df = df.iloc[recommended_indices][['track_name', 'artists', 'track_genre']]

    if show_matches:
        genre_dist = result_df['track_genre'].value_counts()
        print(f"\nRecommendation genre distribution:")
        for genre, count in genre_dist.head(8).items():
            print(f"  {genre}: {count}")

    return result_df
