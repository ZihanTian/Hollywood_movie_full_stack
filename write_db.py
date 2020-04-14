from app import db, Movie, Genre
from scrape import movie_dict, Genres 



genres_dict = {}
ind = 1 
# create genre table
for genre in Genres:
    genres_dict[genre] = str(ind)
    ind += 1
    to_add = Genre(name=genre)
    db.session.add(to_add)
    db.session.commit()

for key,value in movie_dict.items():
    director = value['director']
    #dire = director.split("\")[0]
    
    movie = Movie(name=value['name'],released_year=value['released_year'],
             director=director,one_sentence=value['one_sentence'])
    genre_list = []
    for genre in value['genres']:
        id_table = int(genres_dict[genre])
        item = Genre.query.filter_by(id=id_table).one_or_none()
        genre_list.append(item)
    #print(len(genre_list))
    movie.genres = genre_list 
    db.session.add(movie)
    db.session.commit()


