from config import Config
from flask import Flask, request, render_template
from flask_wtf import FlaskForm
import os
from wtforms import StringField, SubmitField

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
    submit_france = SubmitField('Name my French town!')
    submit_germany = SubmitField('Name my German town!')
    submit_us = SubmitField('Name my US town!')


def pad_left(prompt):
    """Takes the user input and pads it with 1s to the left up to length 3"""
    if len(prompt) >= 3:
        return prompt
    else:
        return ("1" * (3-len(prompt))) + prompt


def read_local_list(country):
    with open("/home/alexwilkes/namemytown/townlists/"+country+".txt", "r") as fopen:
        towns = fopen.readlines()
    return towns


go_external = False
if go_external:
    print("Downloading fresh external town lists")
    town_lists = {
        "germany": fetch_list_germany(germany_towns_url),
        "england": fetch_list_england(english_towns_url),
        "us": fetch_data_britannica(us_towns_url),
        "france": fetch_data_britannica(france_towns_url),
    }

else:
    print("Using locally stored town lists")
    town_lists = {country: read_local_list(country) for country in ["germany", "england", "us", "france"]}

models = {town: TownLearner(town_lists[town]) for town in town_lists.keys()}

for model in models.keys():
    models[model].fit()


# The only page we serve
@app.route('/', methods=['GET', 'POST'])
def home():
    prompt = request.args.get('prompt')

    # Iterates through the arguments until it finds the country button pressed
    country = "england"  # default
    for arg in request.args:
        if arg[:7] == 'submit_':
            country = arg[7:]

    model = models[country]

    if prompt is not None:
        placeholder = model.generate_n_towns(pad_left(prompt))
    else:
        placeholder = set()

    form = PromptForm()
    return render_template('index.html', title='Name my town', form=form, placeholder=placeholder)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)