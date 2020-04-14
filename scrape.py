from bs4 import BeautifulSoup
import requests
import json
import secret 
api_key = secret.omdb_api_key 
baseurl = 'http://www.omdbapi.com/'

# scape Hollywood's 100 Favorite Films and all genres 

response = requests.get('https://www.hollywoodreporter.com/lists/100-best-films-ever-hollywood-favorites-818512/item/seven-samurai-hollywoods-100-favorite-818479')
soup = BeautifulSoup(response.text,'html.parser')
movies_div = soup.find_all('li',class_='list-item--ordered')

movie_dict = {}
Genres = set()
for ind in range(100):
    #print(ind)
    movie_div = movies_div[ind]
    movie_name = movie_div.find('h1', class_='list-item__title').text.strip()
    year = int(movie_div.find('h2',class_='list-item__deck').text.strip()[1:5])
    media_div = movie_div.find_all('p')
    #print(media_div)
    director = media_div[0].text.strip().split(':')[1].strip()
    if len(media_div[3].text.strip().split(':')) == 1:
        one_sentence = 'Not captured'
    else:
        one_sentence = media_div[3].text.strip().split(':')[1].strip()
    params_dict = {
        'apikey': api_key,
        't': movie_name
    }
    response = requests.get(baseurl, params_dict)
    returned = json.loads(response.text)
    if returned['Response'] == 'False':
        genres = ['No type']
        #print('not found')
    else:
        genres = returned['Genre'].split(',')
    for genre_type in genres:
        Genres.add(genre_type)
    

    

    movie_dict[ind+1] = {
        'rank': ind+1,
        'name': movie_name,
        'released_year': year,
        'director': director,
        'one_sentence': one_sentence,
        'genres': genres 
    }
#print(Genres)    
print(movie_dict)