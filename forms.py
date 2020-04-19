from flask_wtf import Form
from wtforms import StringField, SelectField,RadioField
from wtforms.validators import DataRequired
class SearchForm(Form):
    search_item = StringField('searching item')
    search_by = RadioField('Gender', choices=[('Search by rank', 'rank'), ('Search by title', 'title')],
                                  validators=[DataRequired()])