# Spotify Top Tracks Recommender 🎵

A content-based music recommendation system that analyzes your Spotify listening history and suggests similar songs you might enjoy.



## Features ✨

- 🔐 Secure Spotify OAuth login
- 🎧 View your top 10 most-played tracks
- 🎼 Get personalized song recommendations
- 🔊 Play 30-second song previews
- 🎤 See artist, album, and track information
- 🚀 Smart genre balancing (limits K/J-pop if not dominant in your taste)

## How It Works 🛠️

The system uses a hybrid recommendation approach:

1. **Content Analysis**: Extracts audio features (danceability, energy, etc.) from your top tracks
2. **Text Processing**: Analyzes artist names, genres, and track titles using TF-IDF
3. **Clustering**: Groups similar songs using K-Means clustering
4. **Similarity Matching**: Finds the most similar songs using cosine similarity
5. **Genre Balancing**: Automatically adjusts recommendations based on your music preferences

## Tech Stack 💻

- **Frontend**: Streamlit
- **Backend**: Python
- **Spotify API**: spotipy library
- **Machine Learning**:
  - scikit-learn (NearestNeighbors, KMeans, TF-IDF)
  - pandas/numpy for data processing
- **Data**: Custom dataset with 100,000+ songs

## Installation ⚙️

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/spotify-recommender.git
   cd spotify-recommender

    Install dependencies:
    bash

pip install -r requirements.txt

Set up Spotify API credentials:

    Create an app at Spotify Developer Dashboard

    Add client_id and client_secret to app.py

Run the app:
bash

    streamlit run app.py

File Structure 📂
text

spotify-recommender/
├── app.py                # Main Streamlit application
├── recommender.py        # Recommendation engine
├── dataset.csv           # Music dataset (not included in repo)
├── requirements.txt      # Python dependencies
└── README.md             # This file

Dataset 🔢

The system uses a custom dataset containing:

    100,000+ songs

    Audio features (danceability, energy, etc.)

    Track metadata (artist, album, genre)

    Popularity scores

Note: Due to size, the dataset is not included in the repository.
Customization 🎨

You can adjust the recommendation parameters in recommender.py:
python

# Change these values to tweak recommendations
df['valence'] *= 1.5      # How much to weight mood
df['energy'] *= 1.2       # How much to weight energy
df['popularity'] *= 1.2   # How much to weight popularity
k_j_limit = 2             # Max K/J-pop recommendations for non-fans

Live Demo 🌐

Try the app live at: Streamlit Share
Limitations ⚠️

    Requires Spotify Premium for song previews

    Recommendations are based on a static dataset

    New releases may not be included

Future Improvements 🚧

    Add playlist generation

    Incorporate real-time Spotify data

    Add collaborative filtering

    Improve UI with more visualizations

Contributing 🤝

Pull requests are welcome! For major changes, please open an issue first.
License 📜

MIT
