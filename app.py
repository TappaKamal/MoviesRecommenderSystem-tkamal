import streamlit as st
import pickle
import pandas as pd
import requests
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=35dbc5581825d113ac62d74ab1f6a73d&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path', None)
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w200/{poster_path}"
            return full_path
        else:
            return "https://via.placeholder.com/200"
    except Exception:
        return "https://via.placeholder.com/200"

def recommend(movie):
    try:

        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_names.append(movies.iloc[i[0]].title)
            recommended_movie_posters.append(fetch_poster(movie_id))
        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return [], []


# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app title and custom CSS for background color
st.markdown("""
    <style>
    body {
        background-color: #f0f0f0;
    }
    .stButton>button {
        background-color: #FF5733;
        color: white;
    }
    .poster-name {
        display: flex;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit title
st.title("Movie Recommender System")

# Dropdown for movie selection
selected_movie_name = st.selectbox('Welcome! Select a Movie', movies['title'].values)

# Button for recommendations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    if recommended_movie_names:
        # Display movies and posters with name beside the poster
        for i in range(5):
            col1, col2 = st.columns([1, 3])  # Adjust column width ratios as needed
            with col1:
                st.image(recommended_movie_posters[i], width=150)  # Set a fixed width for the poster
            with col2:
                st.markdown(f"**{recommended_movie_names[i]}**")  # Display the movie name in bold

# Footer
        st.write("\nMade With Love By KAMAL HUSSAIN\n")
