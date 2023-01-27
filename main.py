import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID = "Your_client_id_here"
CLIENT_SECRET = "Your_client_secret_here"
REDIRECT_URI = "http://localhost:8888/callback"

date = input("Which date do you want to listen to music from? Type the date in this format YYYY-MM-DD:")
# 2000-08-12
URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(URL)
top_100_wb = response.text

class_no1 = "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet"
#///////////////////////////////class could changes with website updates/////////////////////////////
# c-title  a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet
class_no2to100 = "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only"
#///////////////////////////////class could changes with website updates/////////////////////////////
# c-title  a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only

soup = BeautifulSoup(top_100_wb, "html.parser")
song_names = soup.find_all(
    'h3', attrs={'class': [class_no1, class_no2to100]})

top_100_songs = [song.getText().strip() for song in song_names]
# print(top_100_songs)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope='playlist-modify-private',
                                               show_dialog=True,
                                               cache_path="token.txt"
                                               ))

user_id = sp.current_user()["id"]
songs_uri = []
year = date.split("-")[0]

for song in top_100_songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# creating a new playlist in spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False,)

# adding songs to the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uri)
