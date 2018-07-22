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

#target=np.ones((v_length,1),dtype=np.int8)
#training_data["target"]=target


from sklearn.cluster import KMeans
wcss=[]

X=training_data.iloc[:,[4,12]]  #[0,2,4,6,8,9,11,12,17]

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_scaled = sc.fit_transform(X)


for i in range(1,11):
    kmeans=KMeans(n_clusters=i, init='k-means++',max_iter=300, n_init=10, random_state=0)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)
    
    
plt.plot(range(1,11),wcss)
plt.title('elbow method')
plt.xlabel('# of clusters')

kmeans=KMeans(n_clusters=3, init='k-means++',max_iter=300, n_init=10, random_state=0)

y_kmeans = kmeans.fit_predict(X_scaled)

#my_taste=[]
#i=0
#for song in SavedSongIDs:
#    my_taste.append([sp.track(song)["artists"][0]["name"], sp.track(song)["name"],y_kmeans[i]])
#    i+=1

   
 X_scaled["cluster"]=y_kmeans

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

X=X.values

plt.scatter(X_scaled[y_kmeans == 0, 0],X_scaled[y_kmeans == 0, 1], s= 50, c='red', label='Cluster1')
plt.scatter(X_scaled[y_kmeans == 1, 0],X_scaled[y_kmeans == 1, 1], s= 50, c='blue', label='Cluster2')
plt.scatter(X_scaled[y_kmeans == 2, 0],X_scaled[y_kmeans == 2, 1], s= 50, c='green', label='Cluster3')
plt.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,1], s=150, c='black', label='Centroids')
plt.title('Cluster of clients')
plt.xlabel('energy')
plt.ylabel('tempo')
plt.legend
plt.show



