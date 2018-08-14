# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 17:16:44 2018

@author: Ahmet
"""
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import requests
import numpy as np


import pandas as pd
import IPython.display as ipd
import librosa
import librosa.display

import glob 
import matplotlib.pyplot as plt
import random


#1. Authentication Part
cid = input("Please enter your client id here: ")
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

mfccs=[]
#Getting the previews for the songs liked
os.chdir('C:\\Users\\Ahmet\\Desktop\\machine learning\\Convolutional_Neural_Networks\\audio_dataset\\liked2')
songNum=0
audio_data=[]
for v_offset in range(0,v_length+20,20):
    print(v_offset)
    SavedTracks=sp.current_user_saved_tracks(limit=20,offset=v_offset)
    SavedSongs=SavedTracks["items"]
    for song in SavedSongs:
        if song['track']['preview_url'] is None:
            None
        else:
            songNum=songNum+1
            #SavedSongURLs.append(song['track']['preview_url'])
            #download_file(song['track']['preview_url'],'song'+(str(songNum)))
            audio_data.append(librosa.load('C:\\Users/Ahmet/Desktop/machine learning/Convolutional_Neural_Networks/audio_dataset/liked2/song'+str(songNum)+'.wav'))
            mfccs.append(np.mean(librosa.feature.mfcc(y=audio_data[songNum-1][0], sr=audio_data[songNum-1][1], n_mfcc=40).T,axis=0))
            

np.save('mfccs_array',mfccs)


songNum=186        
#Getting the songs and their features from my DislikedSongs playlist
#Not much different than the upper
myDislikePl= sp.user_playlist(user=username, playlist_id='0ij13jfgJQg3rvyA6T19hP?')

os.chdir('C:\\Users\\Ahmet\\Desktop\\machine learning\\Convolutional_Neural_Networks\\audio_dataset\\disliked2')
DislikedSongsURLs=[]
v_length2=myDislikePl["tracks"]["total"]

for v_dlTrack in myDislikePl["tracks"]["items"]:
    print(songNum)
    if v_dlTrack['track']['preview_url'] is None:
            None
    else:
            songNum=songNum+1
            #DislikedSongsURLs.append(v_dlTrack["track"]["preview_url"])
            #download_file(v_dlTrack['track']['preview_url'],'song'+(str(songNum)))
            #audio_data.append(librosa.load('C:\\Users/Ahmet/Desktop/machine learning/Convolutional_Neural_Networks/audio_dataset/disliked2/song'+str(songNum)+'.wav'))
            mfccs.append(np.mean(librosa.feature.mfcc(y=audio_data[songNum-1][0], sr=audio_data[songNum-1][1], n_mfcc=40).T,axis=0))
      
#librosa audio object
ipd.Audio('C:\\Users/Ahmet/Desktop/machine learning/Convolutional_Neural_Networks/audio_dataset/liked/24HoursIstanbul.wav')

np.save('mfccs_array',mfccs)
np.savetxt("mfccs_array.csv", mfccs, delimiter=" ")

data_dir='C:\\Users\\Ahmet\\Desktop\\machine learning\\Convolutional_Neural_Networks\\audio_dataset\\liked2'

#########buralarda başladı

X = pd.DataFrame(data=mfccs)
Y=np.ones(184) #sevdiklerim
Y=np.append(np.ones(184),np.zeros(30)) #sevmediklerim

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


# Part 1 - Building the CNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Activation
from keras.layers import Dropout
from keras.utils import np_utils




#Building process
clf = Sequential()

clf.add(Dense(256, input_shape=(40,)))
clf.add(Activation('relu'))
clf.add(Dropout(0.5))

clf.add(Dense(256))
clf.add(Activation('relu'))
clf.add(Dropout(0.5))

clf.add(Dense(1))
clf.add(Activation('softmax'))

clf.compile(loss='binary_crossentropy', metrics=['accuracy'], optimizer='adam')
#Building process finishes


clf.fit(X_train, y_train, epochs=25, validation_data=(X_test, y_test))#bunu karşılaştır

y_pred=clf.predict(X_train)

from sklearn.metrics import confusion_matrix

cm=confusion_matrix(y_train,y_pred)
score = clf.evaluate(X_test, y_test)


Y_pred = clf.predict_generator(aaa,validation_data=(X_test, y_test))
y_pred = np.argmax(Y_pred, axis=1)