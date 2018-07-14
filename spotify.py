# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 01:56:35 2018

@author: Ahmet
"""


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util


#1. Authentication Part
cid ="728597db852d430b8dc789cd1e709fdc" 
secret = "bf643e8ed0ed4803b3a251ed651eb9fb"
username = "11155653769"
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
#scope = 'user-library-read playlist-read-private'
 scope = 'playlist-modify-public '
        scope += 'user-library-read '
        scope += 'user-follow-read '
        scope += 'user-library-modify '
        scope += 'user-read-private '
        scope += 'user-top-read'
        
token = util.prompt_for_user_token(username, scope,cid,secret,redirect_uri='http://localhost:8888')

#2. Inputting the model

    #Bossa Nueba Playlist'i üzerinden gideceğiz
fine_playlist = sp.user_playlist("11155653769", "2SjiZrFhqsDtgimUCcCkWB")
fine_tracks = fine_playlist["tracks"]
fine_songs = fine_tracks["items"]

while fine_tracks['next']:
    fine_tracks = sp.next(fine_tracks)
    for item in fine_tracks["items"]:
        fine_songs.append(item)

    #    
fine_ids = [] 
print(len(fine_songs))

for i in range(len(fine_songs)):
    fine_ids.append(fine_songs[i]['track']['id'])       

features = []

for i in range(0,len(fine_ids),50):
    audio_features = sp.audio_features(fine_ids[i:i+50])
    for track in audio_features:
        features.append(track)
        features[-1]['target'] = 1
                
    
#3. Descriptive Statistics
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

trainingData = pd.DataFrame(features)

plt.ylabel('Acousticness')
plt.title('Acousticness of my playlist')
plt.grid(True)
plt.hist(trainingData["acousticness"], facecolor='green')
plt.show()

plt.hist(trainingData["liveness"], facecolor='green')
plt.hist(trainingData["instrumentalness"], facecolor='green')


#4. Where Machine Learning begins
len(sp.current_user_saved_tracks())

#5. Kaldığım yer Songs olarak kaydettiğim library'den limit20'ye takılmadan tüm veriyi almak
sp = spotipy.Spotify(auth=token)
results2 = sp.current_user_saved_tracks(limit=20,offset=20)
i=1
str(i)
for item in results2['items']:
        track = item['track']
        print(str(i) + ' - ' + track['name'] + ' - ' + track['artists'][0]['name'])
        i +=1
     
