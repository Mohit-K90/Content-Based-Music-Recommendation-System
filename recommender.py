import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv("dataset.csv")
df.dropna(subset=['track_name', 'track_genre'], inplace=True)
df.reset_index(drop=True, inplace=True)


track_index = {name.lower(): i for i, name in enumerate(df['track_name'])}


numerical_features = [
    'popularity', 'duration_ms', 'danceability', 'energy', 'key',
    'loudness', 'mode', 'speechiness', 'acousticness',
    'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature'
]


scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[numerical_features])


genre_dummies = pd.get_dummies(df['track_genre'].str.lower(), prefix="genre")


final_song_vectors = np.hstack((scaled_features, genre_dummies.values))

# Recommender function
def recommend_songs(liked_songs, top_n=10):
    liked_indices = [track_index[name.lower()] for name in liked_songs if name.lower() in track_index]

    if not liked_indices:
        return "No liked songs found in dataset."

    liked_vectors = final_song_vectors[liked_indices]
    user_profile = np.asarray(liked_vectors.mean(axis=0)).reshape(1, -1)

    similarities = cosine_similarity(user_profile, final_song_vectors)
    ranked_indices = similarities.argsort()[0][::-1]

    seen_names = set()
    recommended_indices = []

    excluded_genres = {'j-pop', 'jrock', 'j-rock', 'jpop'}  # be safe with variations

    for i in ranked_indices:
        name = df.iloc[i]['track_name']
        genre = str(df.iloc[i]['track_genre']).lower()

        if i in liked_indices or name in seen_names:
            continue
        if any(excluded in genre for excluded in excluded_genres):
            continue

        seen_names.add(name)
        recommended_indices.append(i)
        if len(recommended_indices) == top_n:
            break

    return df.iloc[recommended_indices][['track_name', 'artists', 'track_genre']]
