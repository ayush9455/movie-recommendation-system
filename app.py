import pickle
import streamlit as st
import numpy as np
import pandas as pd
import requests

latent_matrix_df = pickle.load(open('content.pkl','rb'))
latent_matrix_2_df = pickle.load(open('collabrative.pkl','rb'))
link = pickle.load(open('link.pkl','rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    from sklearn.metrics.pairwise import cosine_similarity
    a_1 = np.array(latent_matrix_df.loc[movie]).reshape(1, -1)
    a_2 = np.array(latent_matrix_2_df.loc[movie]).reshape(1, -1)
    score_1 = cosine_similarity(latent_matrix_df, a_1).reshape(-1)
    score_2 = cosine_similarity(latent_matrix_2_df, a_2).reshape(-1)
    hybrid = ((score_1 + score_2) / 2.0)
    dictDf = {'content': score_1, 'collabrative': score_2, 'hybrid': hybrid}
    similar = pd.DataFrame(dictDf, index=latent_matrix_df.index)
    similar.sort_values('hybrid', ascending=False, inplace=True)
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in similar[1:10].index:
        index = link[link['title'] == i].index[0]
        id=link.iloc[index]['tmdbId']
        recommended_movie_posters.append(fetch_poster(id))
        recommended_movie_names.append(i)
    return recommended_movie_names,recommended_movie_posters

st.set_page_config(page_title='Movie Recommendation System')
st.title('Movie Recommender System')
st.image('image.png')
movie_list = link['title']
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
if st.button('Show Recommendations'):
    with st.spinner(text='Loading !!!'):
        recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
        col1, col2, col3, col4 = st.columns(4)
        col5, col6, col7, col8 = st.columns(4)
        with col1:
            st.image(recommended_movie_posters[0])
            st.text(recommended_movie_names[0])
        with col2:
            st.image(recommended_movie_posters[1])
            st.text(recommended_movie_names[1])
        with col3:
            st.image(recommended_movie_posters[2])
            st.text(recommended_movie_names[2])
        with col4:
            st.image(recommended_movie_posters[3])
            st.text(recommended_movie_names[3])
        with col5:
            st.image(recommended_movie_posters[4])
            st.text(recommended_movie_names[4])
        with col6:
            st.image(recommended_movie_posters[5])
            st.text(recommended_movie_names[5])
        with col7:
            st.image(recommended_movie_posters[6])
            st.text(recommended_movie_names[6])
        with col8:
            st.image(recommended_movie_posters[8])
            st.text(recommended_movie_names[8])
hide_menu_style="""
    <style>
    #MainMenu{visibility :hidden;}
    footer{visibility :hidden;}
    </style>
    """
st.markdown(hide_menu_style,unsafe_allow_html=True)