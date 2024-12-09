import streamlit as st
import pickle
import pandas as pd
# Define the recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    for i in movies_list:
        movie_id = i[0]
        #poster nikalo  from api se
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies
# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
# Streamlit app title
st.title("Movie Recommender System")
# Dropdown for movie selection
selected_movie_name = st.selectbox('Welcome! Select a Movie',
                                   movies['title'].values)
# Button for recommendations
if st.button("Recommand"):
    recomdations = recommend(selected_movie_name)
    for i in recomdations:
        st.write(i)
    st.write("\nThank You For Using this!\n")
    st.write("\nMade With Love By KAMAL HUSSAIN\n")