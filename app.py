from config import Config
from flask import Flask, request, render_template

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField

from townlearner import TownLearner
from scraper import (
    english_towns_url,
    fetch_list_england,
    us_towns_url,
    fetch_data_britannica,
    france_towns_url,
    germany_towns_url,
    fetch_list_germany,
)


app = Flask("namemytown")
app.config.from_object(Config)


class PromptForm(FlaskForm):
    prompt = StringField("It works best when you give it a few letters to start with...")
    submit_england = SubmitField('Name my English town!')
    submit_us = SubmitField('Name my US town!')
    submit_france = SubmitField('Name my French town!')
    submit_germany = SubmitField('Name my German town!')


def pad_left(prompt):
    """Takes the user input and pads it with 1s to the left up to length 3"""
    if len(prompt) >= 3:
        return prompt
    else:
        return ("1" * (3-len(prompt))) + prompt


# Train the english town names model
english_town_names = fetch_list_england(english_towns_url)
english = TownLearner(english_town_names)
english.fit()

us_town_names = fetch_data_britannica(us_towns_url)
us = TownLearner(us_town_names)
us.fit()

france_town_names = fetch_data_britannica(france_towns_url)
france = TownLearner(france_town_names)
france.fit()

germany_town_names = fetch_list_germany(germany_towns_url)
germany = TownLearner(germany_town_names)
germany.fit()


# The only page we serve
@app.route('/', methods=['GET', 'POST'])
def home():
    prompt = request.args.get('prompt')

    if "submit_us" in request.args:
        placeholder = us.generate_n_towns(pad_left(prompt))
    elif "submit_england" in request.args:
        placeholder = english.generate_n_towns(pad_left(prompt))
    elif "submit_france" in request.args:
        placeholder = france.generate_n_towns(pad_left(prompt))
    elif "submit_germany" in request.args:
        placeholder = germany.generate_n_towns(pad_left(prompt))
    else:
        placeholder = set()

    form = PromptForm()
    return render_template('index.html', title='Name my town', form=form, placeholder=placeholder)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)