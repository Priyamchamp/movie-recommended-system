import pickle
import streamlit as st
import requests
import pandas as pd
# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies = []
    recommend_movies_poster = []
    for i in movie_list:
        movie_id = i[0]
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_poster.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_poster

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/550{movie_id}?api_key=df50d87487dddaa76f91c19ec6081749"
    response = requests.get(url)
    data = response.json()
    try:
        poster_path = data.get('poster_path')
        if poster_path:
            poster_url = "https://image.tmdb.org/t/p/w500/" + poster_path
            return poster_url
        else:
            print("Poster path not found or empty for movie ID:", movie_id)
            # Return a placeholder image URL
            return "https://via.placeholder.com/500x750.png?text=Poster+Not+Available"
    except Exception as e:
        print("Error fetching poster for movie ID:", movie_id, "Error:", e)
        # Return a placeholder image URL
        return "https://via.placeholder.com/500x750.png?text=Error"


# Load the movies data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set the title of the app
st.title('Movie Recommended System')

# Set a background color
st.markdown(
    """
    <style>
    body {
        background-color: #f0f0f0; /* Light grey */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create a select box to select a movie
options = st.selectbox('Type the Name of the movie you want', movies['title'].values)
if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(options)
    for name, poster in zip(recommended_movie_names, recommended_movie_posters):
        st.text(name)
        st.image(poster)
