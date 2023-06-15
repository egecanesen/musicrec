import streamlit as st
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np
import os

st.markdown("# Manual Search With Song Attributes")
st.sidebar.markdown("""
                    # Manual Search
                    This module uses a Nearest Neighbor model to find songs that 
                    have similar attributes to the attributes that are selected.

                    ## How to use?
                    - Wait for the data to load.
                    - Change the attributes according to your needs.
                    - Select which attributes you care about! (Model ignores unselected attributes)
                    - Input how many songs you want to get as recommendations. (default=50)
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

song_attributes = ['explicit', 'key', 'mode', 'time_signature', 'duration_ms',
                    'danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                    'instrumentalness', 'liveness', 'valence', 'tempo']



st.markdown("## General Features")

explicit = st.selectbox("Content", ("Explicit", "Not Explicit"))

if explicit == "Explicit":
    explicit_choice = 1
elif explicit == "Not Explicit":
    explicit_choice = 0

st.write("The key the track is in. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1.")

key = st.slider('key',  -1, 11, 1)

st.write("Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.")

mode = st.slider('mode',  0, 1, 0)

st.write('An estimated time signature. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure). The time signature ranges from 3 to 7 indicating time signatures of "3/4", to "7/4".')

time_signature = st.slider('time_signature',  0, 4, 4)

duration_sec = st.slider('duration (in seconds)', 0, 900, 200)

st.write(f"The selected duration is {(duration_sec / 60):.2f} minutes")


st.markdown("## Song Attributes")

st.write("Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.")


danceability = st.slider('danceability', 0.0, 1.0, 0.5)

st.write("Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.")

energy = st.slider('energy',  0.0, 1.0, 0.5)

st.write("The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db.")

loudness = st.slider('loudness', -60, 8, 0)

st.write("Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.")

speechiness = st.slider('speechiness',  0.0, 1.0, 0.5)

st.write("A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.")

acousticness = st.slider('acousticness',  0.0, 1.0, 0.5)

st.write('Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.')

instrumentalness = st.slider('instrumentalness',  0.0, 1.0, 0.5)

st.write("Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.")

liveness = st.slider('liveness', 0.0, 1.0, 0.5)

st.write("A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).")

valence = st.slider('valence',  0.0, 1.0, 0.5)

st.write("The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.")

tempo = st.slider('tempo',  0, 250, 100)

options = st.multiselect("Select the categories for your search to consider", song_attributes)


selections_dict = {
    "explicit": explicit_choice,
    "key": key,
    "mode": mode,
    "time_signature": time_signature,
    "duration_ms": duration_sec*1000,
    "danceability": danceability,
    "energy": energy,
    "loudness": loudness,
    "speechiness": speechiness,
    "acousticness": acousticness,
    "instrumentalness": instrumentalness,
    "liveness": liveness,
    "valence": valence,
    "tempo": tempo
}

print(selections_dict)



def recommend_songs(options, n_recommend):

    tempdf = st.session_state['datameans'][options]

    selections_array = []
    for col in tempdf:
        selections_array.append(selections_dict[col])

    selections_array = np.array(selections_array).reshape(1, -1)


    model = NearestNeighbors(n_neighbors=n_recommend)
    model.fit(tempdf)

    neighbors = model.kneighbors(selections_array)
    selected_song_index = neighbors[1][0]


    return st.session_state['datameans'].iloc[selected_song_index][['name', 'artists', 'explicit', 'danceability',
                                                                    'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                                                                    'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms',
                                                                    'time_signature', 'release_date']].reset_index(drop=True)

n_recommend = st.number_input('Select How Many Recommendations You Want: ', value=100)

if st.button('Recommend Songs') and n_recommend:
    with st.spinner('Wait for the model to run...'):
        st.session_state['currentrecommendations'] = recommend_songs(options, int(n_recommend))

if 'currentrecommendations' in st.session_state:
    st.write(st.session_state['currentrecommendations'])
