"""
# My first app
Here's our first attempt at using data to create a table:
"""


import streamlit as st
import pandas as pd
import numpy as np


st.markdown("# Intelligent Music Recommender 🎵")
st.sidebar.markdown("# Main page 🎵")


st.sidebar.success("Select a module above.")

st.markdown(
        """
        This is a music recommendation app that you can control!
        It has three parts:

        1) (word2vec) Million Playlist Dataset Collaborative Filtering
        In this module, a recommendation is done using the million
        playlist dataset. A word2vec algorithm is learned from the playlists
        in the dataset and this model is used to get similar (or dissimilar) 
        songs to the selected songs.

        2) (manualselection) Manual Music Recommendation Using Content Based Filtering
        In this module, you can select the search for songs that have
        song attributes similar to your selection. You can also select which
        attributes should be considered when producing the recommendations.

        3) (attributes) Automatic Music Recommendation Using Content Based Filtering
        This module is similar to the previous module in terms of the recommendation
        algorithm, however this one uses a song selection to get attributes.


        ### References
        - Spotify Million Playlist Dataset [million playlist dataset](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge)
        - Popular Songs Datasets [dataset1](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks) [dataset2](https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs)
        - Streamlit [documentation](https://docs.streamlit.io)
        """
        )




