# Content-Based Music Recommendation System

This is a Streamlit app that uses a content-based filtering approach to recommend songs based on your top Spotify tracks.

##  Features

- Authenticates using your Spotify account.
- Fetches your top 10 most played tracks (medium term).
- Analyzes your musical taste using features like genre, energy, valence, etc.
- Recommends 10 songs from a local dataset that best match your preferences.
- Displays album art, song previews, artist and album info.
- Lets you logout with a single click.

##  How It Works

1. **TF-IDF Vectorization** is applied on text fields like genre and artist names.
2. **Numerical features** like energy, valence, popularity are scaled and weighted.
3. A **user preference vector** is built from your top tracks.
4. **Cosine similarity** is used to rank all songs in the dataset against this vector.
5. Songs with similar names, already liked, or in Japanese genres (J-Pop, J-Rock) are filtered out.

## 🛠️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/music-recommender
cd music-recommender
