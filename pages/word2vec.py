import streamlit as st
from streamlit_searchbox import st_searchbox
from gensim.models import Word2Vec
from typing import List
import pandas as pd
import pickle
import os


st.markdown("# Music Recommendation Using Spotify Million Playlist Dataset")
st.sidebar.markdown("""
                    # Word2Vec
                    This module uses a word2vecv model where
                    each playlist is treated as a "sentence" and each 
                    song is treated as a "word".

                    ## How to use?
                    - Wait for the model to load.
                    - Search the song database of ~1.2 million songs to find stuff you like (or dislike)!
                    """)

#st.markdown(
#        """
#        ## How to use?
#        - Wait for the model to load.
#        - Search the song database of ~1.2 million songs to find stuff you like (or dislike)!
#        - Rate each song in the list easily on the data table
#        - Add / Delete songs from the list
#        """
#        )


EPOCHS = 8
VECTOR_SIZE = 128
SKIPGRAM = True
WINDOW = 16
MIN_COUNT = 1

app_location = os.getcwd()


# Load Model
if 'model' not in st.session_state:

    with st.spinner('Wait for the model to load...'):


        if SKIPGRAM:
            model_name = f"{app_location}/skipgram_epochs{EPOCHS}_vectorsize{VECTOR_SIZE}_window{WINDOW}_mincount{MIN_COUNT}_FINAL.model"
        else:
            model_name = f"{app_location}/cbow_epochs{EPOCHS}_vectorsize{VECTOR_SIZE}_window{WINDOW}_mincount{MIN_COUNT}.model"

        model = Word2Vec.load(model_name)
        #st.write("Successfully Read The Model.")
        st.session_state['model'] = model

# Load Song Names
#if 'song_names' not in st.session_state:
#    song_names = pd.read_pickle("/Users/egcanmac/Desktop/COMP 537/music/app/song_names.pkl")
#    st.session_state['song_names'] = song_names


# Load Song Names Dict
if 'dSongNames' not in st.session_state:
    dSongNames = pd.read_pickle(f"{app_location}/dSongNamesFinal.pkl")
    st.session_state['dSongNamesRev'] = {v:k for k,v in dSongNames.items()} # Song Name: Track Uri
    st.session_state['dSongNames'] = dSongNames # Track Uri: Song Name

if 'song_names' not in st.session_state:
    with open(f"{app_location}/song_names_word2vec.pickle", 'rb') as f:
        st.session_state["song_names"] = pickle.load(f)


# Load Song Dict
if 'dSongVocab' not in st.session_state:
    dSongVocab = pd.read_pickle(f"{app_location}/dSongVocabModified2Final.pkl")
    st.session_state['dSongVocabRev'] = {v:k for k,v in dSongVocab.items()} # Song Vocab Id: Track Uri
    st.session_state['dSongVocab'] = dSongVocab # Track Uri: Song Vocab Id




# Create Empty DataFrame
if 'mpd_recommendations' not in st.session_state:
    st.session_state['mpd_recommendations'] = pd.DataFrame(columns=["Song Name", "Artist Name", "Like/Dislike", "Comments (Why did you like/dislike?)"])
    st.session_state['mpd_recommendations']["Song Name"] = st.session_state['mpd_recommendations']["Song Name"].astype("string")
    st.session_state['mpd_recommendations']["Artist Name"] = st.session_state['mpd_recommendations']["Artist Name"].astype("string")
    st.session_state['mpd_recommendations']["Like/Dislike"] = st.session_state['mpd_recommendations']["Like/Dislike"].astype('bool')
    st.session_state['mpd_recommendations']["Comments (Why did you like/dislike?)"] = st.session_state['mpd_recommendations']["Comments (Why did you like/dislike?)"].astype("category")


# Autocomplete search function
def search_names(searchterm, names):
    if not searchterm:
        # May be updated to retun 20 most popular songs from the list
        return []
    return [name for name in names if searchterm.lower() in name.lower()]

def search_names_list(searchterm):
    return search_names(searchterm, st.session_state.song_names)[:20]

selected_value = st_searchbox(
    search_names_list,
    key="song_searchbox",
)


# Added Uris Initialize
if 'added_uris' not in st.session_state:
    st.session_state['added_uris'] = []


if 'recommendations' not in st.session_state:
    st.session_state['recommendations'] = []


#if selected_value != None and selected_value != st.session_state['prev_selected']:
if selected_value != None:
    #print(selected_value)

    index_val = len(st.session_state['mpd_recommendations'])

    selected_tuple = tuple(selected_value.split(' · '))
    #print("HEREREERERERERERERER")
    #print(list(st.session_state['dSongNames'].keys())[:10])

    current_track_uri = st.session_state['dSongNamesRev'][selected_tuple]

    if current_track_uri not in st.session_state['added_uris']:

        st.session_state['added_uris'].append(current_track_uri)

        #selected_value = selected_value.split(" · ")

        
        toadd = {"Song Name": selected_tuple[1],
                "Artist Name": selected_tuple[0],
                "Like/Dislike": True,
                "Comments (Why did you like/dislike?)": "-"}
        
        new_df = pd.concat([st.session_state['mpd_recommendations'], pd.DataFrame(toadd, index=[index_val])])

        st.session_state['mpd_recommendations'] = new_df
        #st.session_state['prev_selected'] = selected_value



@st.cache_data
def get_recommend(pos_list, neg_list, n_recommend):
    model = st.session_state['model']
    return model.wv.most_similar(positive=pos_list, negative=neg_list, topn=n_recommend)

edited_df = st.data_editor(st.session_state['mpd_recommendations'], use_container_width=True, num_rows="dynamic")
st.session_state['mpd_recommendations'] = edited_df



n_recommend = st.number_input('Select How Many Recommendations You Want: ', value=50)


# Get recommendations
if st.session_state['added_uris'] != []:
    if st.button('Recommend Songs'):

        #st.write()

        with st.spinner('Wait for the model to run...'):

            tempdf = st.session_state['mpd_recommendations'].copy()

            tempdf[tempdf["Like/Dislike"] == True].index

            pos_ind = list(tempdf[tempdf["Like/Dislike"] == True].index)
            neg_ind = list(tempdf[tempdf["Like/Dislike"] == False].index)

            pos_list = [st.session_state['dSongVocab'][st.session_state['added_uris'][i]] for i in pos_ind]
            neg_list = [st.session_state['dSongVocab'][st.session_state['added_uris'][i]] for i in neg_ind]

            
            similar_songs = get_recommend(pos_list, neg_list, int(n_recommend))

            similar_songs_uri = [st.session_state['dSongVocabRev'][i[0]] for i in similar_songs]

            similar_song_names = [st.session_state['dSongNames'][i] for i in similar_songs_uri]

            st.session_state['recommendations'].append(pd.DataFrame(similar_song_names).rename(columns={0: "Artist Name", 1: "Song Name"}))





if st.session_state['recommendations'] != []:
    st.write(st.session_state['recommendations'][-1])
    #st.download_button(
    #label="Download recommendations as CSV",
    #data=st.session_state['recommendations'][-1],
    #file_name='module1recommendations.csv',
    #mime='text/csv')

            

# Display DataFrame
#st.write(st.session_state['mpd_recommendations'])


