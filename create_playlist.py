import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Song import Song

CLIENT_ID = "~"
CLIENT_SECRET = "~"
REDIRECT_URL = "http://localhost:8888/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URL,
                                               scope="playlist-modify-public"))


def get_song_id(song_name, artist_name=None):
    query = f"track:{song_name}"
    if artist_name:
        query += f" artist:{artist_name}"
    
    results = sp.search(q=query, type='track', limit=1)
    tracks = results.get('tracks', {}).get('items', [])
    
    if tracks:
        return tracks[0]['id']
    else:
        print(f"Song '{song_name}' not found. Please check the name and try again.")
        return None


def get_song_recommendations(seed_song_ids, limit=30):
    recommendations = sp.recommendations(seed_tracks=seed_song_ids[:5], limit=limit)
    track_ids = [track['id'] for track in recommendations['tracks']]
    
    return track_ids


def create_playlist_with_recommendations(track_ids, playlist_name="Spotipy Test"):
    user_id = sp.me()['id']
    
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    playlist_id = playlist['id']
    
    sp.playlist_add_items(playlist_id, track_ids)
    
    print(f"Playlist '{playlist_name}' created with {len(track_ids)} songs!")
    print(f"View your playlist here: {playlist['external_urls']['spotify']}")


song_names = input("Enter the names of up to 5 songs, separated by commas: ").split(',')
song_names = [name.strip() for name in song_names if name.strip()]

seed_song_ids = []
for song_name in song_names[:5]:
    artist_name = input(f"Enter the artist name for '{song_name}' (optional): ")
    song_id = get_song_id(song_name, artist_name)
    if song_id:
        seed_song_ids.append(song_id)

if seed_song_ids:
    recommended_track_ids = get_song_recommendations(seed_song_ids)
    playlist_name = input("What name would you like to give to this playlist?: ").strip()
    create_playlist_with_recommendations(recommended_track_ids, playlist_name=playlist_name)
else:
    print("Could not retrieve recommendations due to missing seed song IDs.")
