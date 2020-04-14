import plotly.graph_objs as go 
from app import db, Movie, Genre
xval = []
yval = []
genres = Genre.query.all()
for genre in genres:
    xval.append(genre.name)
    yval.append(len(genre.movies)) 


bar_data = go.Bar(x=xval, y=yval)
basic_layout = go.Layout(title="Numbers of movies in different types")
fig = go.Figure(data=bar_data, layout=basic_layout)

fig.write_html("scatter.html", auto_open=False)
