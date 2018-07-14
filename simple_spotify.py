# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 13:59:29 2018

@author: Ahmet
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util


#1. Authentication Part
cid =<cid>
secret = <secret>
username = <username>
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

sp = spotipy.Spotify(auth=token)

#bunu baştan initialize ediyorum.
SavedSongIDs=[]  
v_length=sp.current_user_saved_tracks()["total"]


for v_offset in range(0,v_length+20,20):
    print(v_offset)
    SavedTracks=sp.current_user_saved_tracks(limit=20,offset=v_offset)
    SavedSongs=SavedTracks["items"]
    for song in SavedSongs:
        SavedSongIDs.append(song['track']['id'])   

features = []
audio_features=[]

for i in range(0,v_length,50):
    audio_features=sp.audio_features(SavedSongIDs[i:i+50])
    for track in audio_features:
        features.append(track)
    
import pandas as pd
training_data=pd.DataFrame(features)


import matplotlib.pyplot as plt
plot_column=training_data[input()].name
plt.hist(training_data[plot_column], facecolor='green')
plt.ylabel('# of songs')
plt.title(plot_column +' of my playlist')
plt.grid(True)



plt.show()
    
