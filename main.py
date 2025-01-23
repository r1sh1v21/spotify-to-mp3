import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from urllib.parse import quote
import yt_dlp
import os

SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''

YOUTUBE_API_KEY = ''

def get_spotify_playlist_tracks(playlist_url):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
    ))

    playlist_id = playlist_url.split('/')[-1].split('?')[0]
    results = sp.playlist_tracks(playlist_id)

    tracks = []
    for item in results['items']:
        track = item['track']
        track_name = f"{track['name']} - {', '.join(artist['name'] for artist in track['artists'])}"
        tracks.append(track_name)

    return tracks

def search_youtube(song_name):
    query = quote(song_name)
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={YOUTUBE_API_KEY}&maxResults=1"
    response = requests.get(url)
    data = response.json()

    if 'items' in data and len(data['items']) > 0:
        video_id = data['items'][0]['id']['videoId']
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        return "No video found"

def download_audio_ytdlp(url, output_folder="downloads"):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download complete!")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    playlist_url = input("Enter Spotify playlist URL: ")

    try:
        songs = get_spotify_playlist_tracks(playlist_url)
    except Exception as e:
        print(f"Error fetching Spotify playlist: {e}")
        return

    
    results = {}
    r=[]
    for song in songs:
        link = search_youtube(song)
        results[song] = link
        r.append(link)

    for link in r:
        download_audio_ytdlp(link)

    

if __name__ == "__main__":
    main()
