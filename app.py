from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)
app.jinja_options = {
    'autoescape': False,
    'extensions': [],
}

@app.route('/', methods=['GET'])
def index():
    with open('movies/index.json') as json_file:
        data = json.load(json_file)

    genres = set()
    for item in data:
        movies = item.get('movies', [])
        for movie in movies:
            movie_genres = movie.get('genre', [])
            genres.update(movie_genres)

    return render_template('index.html', genres=sorted(list(genres)))

@app.route('/movies', methods=['POST'])
def movies():
    with open('movies/index.json') as json_file:
        data = json.load(json_file)

    selected_genres = request.form.getlist('genre')
    search_query = request.form.get('search')

    filtered_movies = []
    for item in data:
        movies = item.get('movies', [])
        filtered_movies.extend(filter_movies(movies, selected_genres, search_query))

    if 'X-Requested-With' in request.headers and request.headers['X-Requested-With'] == 'XMLHttpRequest':
        return jsonify({'movies': filtered_movies})
    else:
        return render_template('index.html', genres=get_genre_list(), movies=filtered_movies)

def filter_movies(movies, genres, search_query):
    filtered_movies = []

    for movie in movies:
        movie_genres = movie.get('genre', [])
        movie_title = movie.get('title', '').lower()

        if genres and not any(genre in movie_genres for genre in genres):
            continue

        if search_query and search_query.lower() not in movie_title:
            continue

        filtered_movies.append(movie)

    return filtered_movies

def get_genre_list():
    with open('movies/index.json') as json_file:
        data = json.load(json_file)

    genres = set()
    for item in data:
        movies = item.get('movies', [])
        for movie in movies:
            movie_genres = movie.get('genre', [])
            genres.update(movie_genres)

    return list(genres)

if __name__ == '__main__':
    app.run(debug=True)
