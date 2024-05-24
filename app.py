import streamlit as st
import pickle
import pandas as pd
import requests #library to hit api
def fetchPoster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=da3380e70fd2beebb7280c1db76a593d'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500"+data['poster_path']
movie_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movie_dict)
similarity=pickle.load(open('similarity.pkl','rb'))

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movie_posters=[]

    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        movie_id = movies.iloc[i[0]].movie_id
        #fetch poster from api
        recommended_movie_posters.append(fetchPoster(movie_id))
    return recommended_movies, recommended_movie_posters

st.title('Movie Recommender System')
selectedMovieName = st.selectbox(
    "Select a Movie",
    movies['title'].values)


def centered_text(text):
    return f'<p style="text-align: center;">{text}</p>'

if st.button("Recommend"):
    names, posters=recommend(selectedMovieName)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0])
        st.markdown(centered_text(names[0]), unsafe_allow_html=True)
    with col2:
        st.image(posters[1])
        st.markdown(centered_text(names[1]), unsafe_allow_html=True)
    with col3:
        st.image(posters[2])
        st.markdown(centered_text(names[2]), unsafe_allow_html=True)
    with col4:
        st.image(posters[3])
        st.markdown(centered_text(names[3]), unsafe_allow_html=True)
    with col5:
        st.image(posters[4])
        st.markdown(centered_text(names[4]), unsafe_allow_html=True)