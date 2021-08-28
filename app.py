from io import BytesIO 
from flask import Flask, request, Response, jsonify
from flask.helpers import send_file
from database import init_db
from database.models import Director, Movie, Imdb


app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/test_movie'
}
init_db(app)

# Get all movies


@app.route('/movies/')
def get_movies():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    # movies = Movie.objects()
    # return jsonify(movies)

    movies = Movie.objects.paginate(page=page, per_page=limit)
    return jsonify([movie for movie in movies.items]), 200

# Get one movie


@app.route('/movies/<id>/')
def get_one_movie(id: str):
    # movie = Movie.objects(id=id).first()
    movie = Movie.objects.get_or_404(id=id)
    return jsonify(movie), 200

# Add Movie


@app.route('/movies/', methods=['POST'])
def add_movie():
    director = Director.objects.get(id="600fb8138724900858706a56")
    body = request.get_json()
    movie = Movie(director=director, **body).save()
    return jsonify(movie), 201

# Add Movie


@app.route('/movies-embed/', methods=['POST'])
def add_movie_embed():
    imdb = Imdb(imdb_id="12340mov", rating=4.2, votes=7.9)
    body = request.get_json()
    movie = Movie(imdb=imdb, **body).save()
    return jsonify(movie)


@app.route('/director/', methods=['POST'])
def add_dir():
    body = request.get_json()
    director = Director()
    # director.name = body.get("name")
    # director.age = body.get("age")
    # director.save()

    setattr(director, "name", body.get("name"))
    setattr(director, "age", body.get("age"))
    director.save()

    return jsonify(director)


@app.route('/movies/<id>/', methods=['PUT'])
def update_movie(id):
    body = request.get_json()
    movie = Movie.objects.get_or_404(id=id)
    movie.update(**body)
    return jsonify(str(movie.id)), 200


@app.route('/movies_many/<year>/', methods=['PUT'])
def update_movie_many(year):
    body = request.get_json()
    movies = Movie.objects(year=year)
    movies.update(**body)
    return jsonify([str(movie.id) for movie in movies]), 200


@app.route('/movies/<id>/', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.objects.get_or_404(id=id)
    movie.delete()
    return jsonify(str(movie.id)), 200


@app.route('/movies/delete-by-year/<year>/', methods=['DELETE'])
def delete_movie_by_year(year):
    movies = Movie.objects(year=year)
    movies.delete()
    return jsonify([str(movie.id) for movie in movies]), 200


@app.route('/movies_with_poster/', methods=['POST'])
def add_movie_with_image():
    # 1
    image = request.files['file']

    # 2
    movie = Movie(title="movie with poster", year=2021)

    # 3
    movie.poster.put(image, filename=image.filename)

    # 4
    movie.save()

   # 5
    return jsonify(movie), 201


@app.route('/movies_with_poster/<id>/', methods=['GET'])
def get_movie_image(id):

    # 1
    movie = Movie.objects.get_or_404(id=id)

    # 2
    image = movie.poster.read()
    content_type = movie.poster.content_type
    filename = movie.poster.filename

    # 3
    return send_file(
        # 4
        BytesIO(image),
        attachment_filename=filename,
        mimetype=content_type), 200


@app.route('/movies_with_poster/<id>/', methods=['DELETE'])
def delete_movie_image(id):

    # 1
    movie = Movie.objects.get_or_404(id=id)

    # 2
    movie.poster.delete()

    # 3
    movie.delete()
    return "", 204


if __name__ == "__main__":
    app.run()
