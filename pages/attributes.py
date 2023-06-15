import streamlit as st
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from streamlit_searchbox import st_searchbox
import numpy as np
import pickle
import os



st.markdown("# Search With Song Attributes")
st.sidebar.markdown("""
                    # Attribute Search
                    This module uses a Nearest Neighbor model to find songs that 
                    have similar attributes to the songs that are selected.

                    ## How to use?
                    - Wait for the data to load.
                    - Choose songs.
                    - Select which attributes you care about! (Model ignores unselected attributes)
                    """)


# Load Model
#if 'modelmeans' not in st.session_state:
#    model = pd.read_pickle("modelmeans.pkl")
#    st.write("Successfully Read The Model.")
#    st.session_state['modelmeans'] = model

app_location = os.getcwd()


# Load Data
if 'datameans' not in st.session_state:
    with st.spinner('Wait for the data to load...'):
        st.session_state['datameans'] = pd.read_csv(f"{app_location}/df_featuresFINAL.csv")

if "sattributes" not in st.session_state:
    with open(f"{app_location}/my_list.pickle", 'rb') as f:
        songs_with_attributes = pickle.load(f)
    st.session_state['sattributes'] = songs_with_attributes

song_attributes = ['explicit', 'key', 'mode', 'time_signature', 'duration_ms',
                    'danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                    'instrumentalness', 'liveness', 'valence', 'tempo']


#print(st.session_state['sattributes'][:20])

# Autocomplete search function
def search_names2(searchterm, names):
    if not searchterm:
        # May be updated to retun 20 most popular songs from the list
        return []
    return [name for name in names if str(searchterm).lower() in str(name).lower()]

def search_names_list2(searchterm):
    return search_names2(searchterm, st.session_state.sattributes)[:20]

selected_value2 = st_searchbox(
    search_names_list2,
    key="song_searchbox",
)


if 'spd_recommendations' not in st.session_state:
    st.session_state['spd_recommendations'] = pd.DataFrame(columns=[['name', 'artists', 'explicit', 'danceability',
                                                                    'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                                                                    'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms',
                                                                    'time_signature', 'release_date']])



options = st.multiselect("Select the categories for your search to consider", song_attributes)

# Added Inds Initialize
if 'added_inds' not in st.session_state:
    st.session_state['added_inds'] = []

if selected_value2 != []:

    index_val = st.session_state['sattributes'].index(selected_value2)

    if index_val not in st.session_state['added_inds']:

        st.session_state['added_inds'].append(index_val)

        currentdf = st.session_state['datameans'].iloc[np.array(st.session_state['added_inds'])]
        
        #new_df = pd.concat([st.session_state['spd_recommendations'], pd.DataFrame(toadd)])

        st.session_state['spd_recommendations'] = currentdf[['name', 'artists', 'explicit', 'danceability',
                                                            'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                                                            'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms',
                                                            'time_signature', 'release_date']]


if st.session_state['added_inds'] != []:
    st.write(st.session_state['spd_recommendations'])


selections_dict = {}

for attr in song_attributes:

    selections_dict[attr] = st.session_state['spd_recommendations'][attr].mean()


print(selections_dict)



def recommend_songs(options):

    tempdf = st.session_state['datameans'][options]

    selections_array = []
    for col in tempdf:
        selections_array.append(st.session_state['spd_recommendations'][col].mean())

    selections_array = np.array(selections_array).reshape(1, -1)


    model = NearestNeighbors(n_neighbors=100)
    model.fit(tempdf)

    neighbors = model.kneighbors(selections_array)
    selected_song_index = neighbors[1][0]

    selected_song_index = [i for i in selected_song_index if i not in st.session_state['added_inds']]

    return st.session_state['datameans'].iloc[selected_song_index[:25]]



if st.button('Recommend Songs'):
    st.session_state['meanrecommendation'] = recommend_songs(options)


if 'meanrecommendation' in st.session_state:
    st.write(st.session_state['meanrecommendation'])