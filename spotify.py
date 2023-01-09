import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_playlist_tracks(client_id : str, client_secret : str, playlist_id : str):

  # Set up the Spotify object
  auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
  spotify = spotipy.Spotify(auth_manager=auth_manager)

  # Get the playlist
  playlist = spotify.playlist(playlist_id)

  # Print the playlist name
  print("Playlist", playlist['name'])

  # Print the track list
  return playlist['tracks']['items']