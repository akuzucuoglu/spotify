# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 13:59:29 2018

@author: Ahmet
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util


#1. Authentication Part
cid =input("Please enter your client id here: ")
secret = input("Please enter your secret here: ")
username = input("Please enter your username here: ")
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

#Dataframe creation   
import pandas as pd
training_data=pd.DataFrame(features)

#Simple visualization
import matplotlib.pyplot as plt
plot_column=training_data[input("enter column name for visualization: ")].name
plt.hist(training_data[plot_column], facecolor='green')
plt.ylabel('# of songs')
plt.title(plot_column +' of my playlist')
plt.grid(True)

#Adding a target column
import numpy  as np 

target=np.ones((v_length,1),dtype=np.int8)
training_data["target"]=target


#Getting the songs and their features from my DislikedSongs playlist
#Not much different than the upper
myDislikePl= sp.user_playlist(user=username, playlist_id='0ij13jfgJQg3rvyA6T19hP?')

v_length2=myDislikePl["tracks"]["total"]


DislikedSongsIDs=[]
for v_dlTrack in myDislikePl["tracks"]["items"]:
    print(v_dlTrack["track"]["id"])
    DislikedSongsIDs.append(v_dlTrack["track"]["id"])


dis_features = []
dis_audio_features=[]

for i in range(0,v_length2,50):
    dis_audio_features=sp.audio_features(DislikedSongsIDs[i:i+50])
    for track in dis_audio_features:
        dis_features.append(track)

dis_training_data=pd.DataFrame(dis_features)
target=np.ones((v_length2,int(1)),dtype=np.int8)
dis_training_data["target"]=target


for i in range(v_length2):
    print(i)
    dis_training_data["target"][i]=0

new_training_data=training_data.append(dis_training_data, ignore_index=True)

