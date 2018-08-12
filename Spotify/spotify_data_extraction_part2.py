# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 01:02:07 2018

@author: Ahmet
"""


import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import requests

import pandas as pd
import librosa
import librosa.display
import glob 
import matplotlib.pyplot as plt

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
SavedSongURLs=[]
v_length=sp.current_user_saved_tracks()["total"]


#Defining downloading function
def download_file(url,filename):
    #''.join(fix for fix in filename if fix.isalnum())
    local_filename = ''.join(fix for fix in filename if fix.isalnum()) +'.wav' #url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename



os.chdir('C:\\Users\\Ahmet\\Desktop\\machine learning\\Convolutional_Neural_Networks\\audio_dataset\\liked')
for v_offset in range(0,v_length+20,20):
    print(v_offset)
    SavedTracks=sp.current_user_saved_tracks(limit=20,offset=v_offset)
    SavedSongs=SavedTracks["items"]
    for song in SavedSongs:
        if song['track']['preview_url'] is None:
            None
        else:
            SavedSongURLs.append(song['track']['preview_url'])
            download_file(song['track']['preview_url'],song['track']['name'])


#Getting the songs and their features from my DislikedSongs playlist
#Not much different than the upper
myDislikePl= sp.user_playlist(user=username, playlist_id='0ij13jfgJQg3rvyA6T19hP?')

os.chdir('C:\\Users\\Ahmet\\Desktop\\machine learning\\Convolutional_Neural_Networks\\audio_dataset\\disliked')
DislikedSongsURLs=[]
v_length2=myDislikePl["tracks"]["total"]

for v_dlTrack in myDislikePl["tracks"]["items"]:
    print(v_dlTrack["track"]["preview_url"])
    if v_dlTrack['track']['preview_url'] is None:
            None
    else:
            DislikedSongsURLs.append(v_dlTrack["track"]["preview_url"])
            download_file(v_dlTrack['track']['preview_url'],v_dlTrack['track']['name'])
            
            
import IPython.display as ipd
ipd.Audio('C:\\Users/Ahmet/Desktop/machine learning/Convolutional_Neural_Networks/audio_dataset/liked/YazGazeteciYaz.wav')

import librosa

data, sampling_rate = librosa.load('C:\\Users/Ahmet/Desktop/machine learning/Convolutional_Neural_Networks/audio_dataset/liked/YazGazeteciYaz.wav')



plt.figure(figsize=(12, 4))
librosa.display.waveplot(data, sr=sampling_rate)

data
