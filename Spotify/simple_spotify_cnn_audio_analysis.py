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

import pandas as pd
import IPython.display as ipd
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


#Getting the songs and their features from my DislikedSongs playlist
#Not much different than the upper
myDislikePl= sp.user_playlist(user=username, playlist_id='0ij13jfgJQg3rvyA6T19hP?')

os.chdir('C:\\Users\\Ahmet\\Desktop\\machine learning\\Convolutional_Neural_Networks\\audio_dataset\\disliked2')
DislikedSongsURLs=[]
v_length2=myDislikePl["tracks"]["total"]
for v_dlTrack in myDislikePl["tracks"]["items"]:
    print(v_dlTrack["track"]["preview_url"])
    if v_dlTrack['track']['preview_url'] is None:
            None
    else:
            songNum=songNum+1
            #DislikedSongsURLs.append(v_dlTrack["track"]["preview_url"])
            #download_file(v_dlTrack['track']['preview_url'],'song'+(str(songNum)))
            audio_data.append(librosa.load('C:\\Users/Ahmet/Desktop/machine learning/Convolutional_Neural_Networks/audio_dataset/disliked2/song'+str(songNum)+'.wav'))




 = librosa.load('C:\\Users/Ahmet/Desktop/machine learning/Convolutional_Neural_Networks/audio_dataset/liked2/song'+str(songNum)+'.wav')
      
#librosa audio object
ipd.Audio('C:\\Users/Ahmet/Desktop/machine learning/Convolutional_Neural_Networks/audio_dataset/liked/24HoursIstanbul.wav')

#getting the spectogram out of librosa audio file 
data, sampling_rate = librosa.load('C:\\Users/Ahmet/Desktop/machine learning/Convolutional_Neural_Networks/audio_dataset/liked/24HoursIstanbul.wav')

#drawing the spectogram
plt.figure(figsize=(20, 4))
librosa.display.waveplot(data, sr=sampling_rate)

# Part 1 - Building the CNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Activation
from keras.layers import Dropout

import numpy as np

mfccs = np.mean(librosa.feature.mfcc(y=audio_data[0][0], sr=audio_data[0][1], n_mfcc=40).T,axis=0)

#Building process
classifier = Sequential()

classifier.add(Dense(256, input_shape=(40,)))
classifier.add(Activation('relu'))
classifier.add(Dropout(0.5))

classifier.add(Dense(256))
classifier.add(Activation('relu'))
classifier.add(Dropout(0.5))

classifier.add(Dense(num_labels))
classifier.add(Activation('softmax'))

classifier.compile(loss='binary_crossentropy', metrics=['accuracy'], optimizer='adam')
#Building process finishes


#Part 2. Defining data 
#you define where the training set comes from
#bununla
training_set = train_datagen.flow_from_directory('dataset/training_set',
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'binary')

#you define where the test set comes from
test_set = test_datagen.flow_from_directory('dataset/test_set',
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'binary')

vs
model.fit(X, y, batch_size=32, epochs=5, validation_data=(val_x, val_y))#bunu karşılaştır


#Train model with training set
classifier.fit_generator(training_set,
                         samples_per_epoch = 8000,
                         nb_epoch = 5,
                         validation_data = test_set,
                         nb_val_samples = 2000)

