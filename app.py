import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import time
from urllib.parse import urlparse, parse_qs

from recommender import recommend_songs

st.set_page_config(page_title="Spotify Top Tracks", page_icon="🎵")
st.title("🎵 Your Spotify Top Tracks")

client_id = "c79e5ded82a941ee9f99b45e14173c19"
client_secret = "cc5dafaab5a048c48ee953b6e1472083"
redirect_uri = "http://127.0.0.1:8501"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


# Logout function
def logout():
    # Remove the cache file
    if os.path.exists(".spotifycache"):
        os.remove(".spotifycache")
    st.session_state.logged_in = False
    st.rerun()


# Create authentication manager
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-top-read",
    cache_path=".spotifycache",
    show_dialog=True
)

# Check for authentication code in URL using the new API
code = st.query_params.get("code", None)

# Try to load cached token or authenticate
if os.path.exists(".spotifycache"):
    try:
        token_info = auth_manager.get_cached_token()
        if token_info and token_info.get('access_token'):
            st.session_state.logged_in = True
    except:
        pass

# Handle new authentication with code
if code and not st.session_state.logged_in:
    try:
        # Exchange code for token
        auth_manager.get_access_token(code)
        st.session_state.logged_in = True
        # Clear the URL parameters
        st.query_params.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Authentication error: {e}")

# Display different content based on login state
if not st.session_state.logged_in:
    st.info("Please log in with your Spotify account to view your top tracks and get recommendations.")

    if st.button("Login with Spotify"):
        auth_url = auth_manager.get_authorize_url()
        st.markdown(f"[Click here to login with Spotify]({auth_url})", unsafe_allow_html=True)

else:
    # User is logged in, initialize Spotify client
    try:
        sp = spotipy.Spotify(auth_manager=auth_manager)
        user_info = sp.current_user()

        # Display user info and logout button
        col1, col2 = st.columns([3, 1])
        col1.success(f"Logged in as: {user_info['display_name']}")
        if col2.button("Logout"):
            logout()

        top_tracks = sp.current_user_top_tracks(limit=10, time_range="medium_term")

        if top_tracks and top_tracks['items']:
            st.header("Your Top 10 Tracks")

            liked_song_names = []

            for i, track in enumerate(top_tracks['items'], 1):
                col1, col2 = st.columns([1, 3])

                if track['album']['images']:
                    col1.image(track['album']['images'][0]['url'], width=100)

                artists = ", ".join([artist['name'] for artist in track['artists']])
                col2.subheader(f"{i}. {track['name']}")
                col2.write(f"Artist: {artists}")
                col2.write(f"Album: {track['album']['name']}")

                if track['preview_url']:
                    col2.audio(track['preview_url'], format="audio/mp3")

                liked_song_names.append(track['name'])
                st.divider()

            # Recommendation section
            if st.button("Recommend Songs Based on Your Top Tracks"):
                recs = recommend_songs(liked_song_names, top_n=10)

                if isinstance(recs, str):  # e.g., error message
                    st.warning(recs)
                else:
                    st.header("Recommended Songs")

                    for i, (_, row) in enumerate(recs.iterrows(), 1):
                        col1, col2 = st.columns([1, 3])

                        # Use Spotify API to get track details for visuals
                        try:
                            results = sp.search(q=row['track_name'] + " " + row['artists'], limit=1, type='track')
                            track_info = results['tracks']['items'][0]

                            if track_info['album']['images']:
                                col1.image(track_info['album']['images'][0]['url'], width=100)

                            col2.subheader(f"{i}. {track_info['name']}")
                            col2.write(f"Artist: {row['artists']}")
                            col2.write(f"Album: {track_info['album']['name']}")

                            if track_info['preview_url']:
                                col2.audio(track_info['preview_url'], format="audio/mp3")

                        except Exception as e:
                            col2.subheader(f"{i}. {row['track_name']}")
                            col2.write(f"Artist: {row['artists']}")
                            col2.write("⚠️ Additional data not found via Spotify.")

                        st.divider()

        else:
            st.info("No top tracks found. You might need to use Spotify more to generate this data.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
        # Show logout button in case of errors
        if st.button("Logout"):
            logout()