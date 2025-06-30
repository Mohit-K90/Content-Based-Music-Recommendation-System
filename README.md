# Spotify Music Recommendation System

A content-based music recommender that suggests songs based on your Spotify listening history.

## Features
- View your top 10 Spotify tracks
- Get personalized song recommendations
- Play 30-second song previews
- Secure Spotify login
- Smart genre filtering

## Requirements
- Python 3.7+
- Spotify developer account
- Spotify Premium (for audio previews)

## Installation
1. Clone this repository:

git clone https://github.com/yourusername/spotify-recommender.git
cd spotify-recommender
text


2. Install dependencies:

pip install streamlit spotipy scikit-learn pandas numpy
text


3. Add your Spotify API credentials to app.py:
```python
client_id = "your_client_id"
client_secret = "your_client_secret"
redirect_uri = "your_redirect_uri"

    Run the app:

text

streamlit run app.py

How It Works

    Log in with Spotify

    The app fetches your top 10 tracks

    The recommendation engine analyzes:

        Audio features (danceability, energy, etc.)

        Artist information

        Genre characteristics

    Suggests similar songs from the dataset

Files

    app.py - Main application (Streamlit)

    recommender.py - Recommendation engine

    dataset.csv - Song database

Configuration

Adjust recommendation parameters in recommender.py:
python

# Weight adjustments
df['valence'] *= 1.5  # Mood importance
df['energy'] *= 1.2   # Energy importance

# Genre limits
k_j_limit = 2  # Max K/J-pop recommendations

Notes

    Requires Spotify Premium for audio previews

    Dataset not included (too large for GitHub)

    New songs may not be in recommendations

License

MIT License
text


Just copy everything between (and including) the ``` marks and paste it directly into your README.md file. All formatting will be preserved.

New chat
