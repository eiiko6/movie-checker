from flask import Flask, render_template, jsonify, request
import requests
import config

app = Flask(__name__)

# Global variables to keep track of API pages and current movie index
current_movie_index = 0
movies = []
current_page = 1
total_pages = None


# Fetch movies sorted by revenue
def fetch_movies(page=1):
    global movies, total_pages
    url = f"https://api.themoviedb.org/3/discover/movie?sort_by=revenue.desc&api_key={config.TMDB_API_KEY}&page={page}"
    response = requests.get(url)
    data = response.json()

    # Store the total number of pages available
    total_pages = data["total_pages"]

    for movie in data["results"]:
        movie_details_url = f'https://api.themoviedb.org/3/movie/{movie["id"]}?api_key={config.TMDB_API_KEY}'
        movie_details = requests.get(movie_details_url).json()
        production_companies = movie_details.get("production_companies", [])
        producer = (
            production_companies[0]["name"] if production_companies else "Unknown"
        )

        movies.append(
            {
                "title": movie["title"],
                "popularity": movie["popularity"],
                "box_office": movie_details.get("revenue", "N/A"),
                "runtime": movie_details.get("runtime", "N/A"),
                "release_year": movie["release_date"].split("-")[0],
                "producer": producer,
                "cover": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}",
            }
        )


# Write movie details to a file
def save_movie_to_file(movie):
    file_path = "saved_movies.txt"
    with open(file_path, "a") as f:
        f.write(f"{movie['title']} - {movie['runtime']} minutes\n")


# Route to serve the main page
@app.route("/")
def index():
    global current_movie_index, current_page
    if not movies:
        fetch_movies(current_page)  # Fetch first page of movies initially
    return render_template("index.html", movie=movies[current_movie_index])


# Fetch the next movie or the next page of movies if necessary
def get_next_movie():
    global current_movie_index, current_page, total_pages

    # Move to the next movie
    current_movie_index += 1

    print("current movie:", current_movie_index)
    print("len movies: ", len(movies))

    # If we've run out of movies in the current list, fetch the next page
    if current_movie_index >= len(movies):
        current_page += 1
        if current_page <= total_pages:  # Ensure we don't exceed the available pages
            fetch_movies(current_page)
        else:
            current_page = 1  # Reset to page 1 if we reach the end of all pages

    return movies[current_movie_index]


# Route to handle skipping to the next movie
@app.route("/skip", methods=["POST"])
def skip_movie():
    next_movie = get_next_movie()
    return jsonify(next_movie)


# Route to save the movie and move to the next one
@app.route("/save", methods=["POST"])
def save_movie():
    global current_movie_index
    movie = movies[current_movie_index]
    save_movie_to_file(movie)
    next_movie = get_next_movie()
    return jsonify(next_movie)


if __name__ == "__main__":
    app.run(debug=True)
