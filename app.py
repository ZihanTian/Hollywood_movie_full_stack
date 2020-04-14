from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
import json
import sys
import os
import secret 
import plotly.graph_objs as go 
from flask_wtf import Form
from forms import *

api_key = secret.omdb_api_key 
baseurl = 'http://www.omdbapi.com/'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zihantian@localhost:5432/movieapp'

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)
migrate = Migrate(app, db)

CACHE_FILENAME = "movie_cache.json"
CACHE_DICT = {}
def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

movie_genres = db.Table('movie_genres',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.rank'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

class Movie(db.Model):
    rank = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    released_year = db.Column(db.Integer,nullable=False)
    director = db.Column(db.String(), nullable=False)
    one_sentence = db.Column(db.String(), nullable=False)
    genres = db.relationship('Genre',secondary='movie_genres',
        backref=db.backref('movies'))

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)

# return all genres and all 100 movies 
def format_genre(genre_class):
    genre = {}
    genre['id'] = genre_class.id 
    genre['name'] = genre_class.id 
    return genre 

def format_movie(movie_class):
    movie = {}
    movie['rank'] = movie_class.rank 
    movie['name'] = movie_class.name 
    movie['released_year'] = movie_class.released_year
    movie['director'] = movie_class.director 
    movie['one_sentence'] = movie_class.one_sentence
    return movie 
@app.route('/genres/<genre_id>')
def get_genre_movies(genre_id):
    form = SearchForm()
    genre = Genre.query.filter_by(id=genre_id).one_or_none()
    movies_selection = genre.movies 
    movies = [format_movie(movie_class) for movie_class in movies_selection]
    genres_selection = Genre.query.all()
    genres = [format_genre(genre_class) for genre_class in genres_selection]
    active_genre = Genre.query.get(genre_id)
    return render_template('index.html', genres=genres_selection, movies=movies, active_genre=active_genre,form=form)

@app.route('/')
def index():
    return redirect(url_for('get_genre_movies', genre_id=1))

@app.route('/movies/<movie_id>')
def get_movie_detail(movie_id):
    
    movie = Movie.query.get(movie_id)
    params_dict = {
        'apikey': api_key,
        't': movie.name
    }
    
    # use cache here: get ratings from ratings from cache first, if not fetch form api
    cache_dict = open_cache()
    if str(movie_id) in cache_dict:
        ratings = cache_dict[str(movie_id)]
    else:
        response = requests.get(baseurl, params_dict)
        returned = json.loads(response.text)
        ratings = {}

        if returned['Response'] != 'False':
            api_ratings = returned["Ratings"]
            for item in api_ratings:
                ratings[item["Source"]] = item["Value"]
        cache_dict[str(movie_id)] = ratings 
        save_cache(cache_dict)
    one_sentence = movie.one_sentence
    return render_template('movie_detail.html',movie_name=movie.name,one_sentence=one_sentence,ratings=ratings)

@app.route("/plot")
def plot_image():
    return render_template("scatter.html")
    
    