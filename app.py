from config import Config
from flask import Flask, request, render_template

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from townlearner import TownLearner
from scraper import english_towns_url, fetch_list


app = Flask("namemytown")
app.config.from_object(Config)


class PromptForm(FlaskForm):
    prompt = StringField("It works best when you give it a few letters to start with...")
    submit = SubmitField('Now name my town!')


def pad_left(prompt):
    """Takes the user input and pads it with 1s to the left up to length 3"""
    if len(prompt) >= 3:
        return prompt
    else:
        return ("1" * (3-len(prompt))) + prompt


# Train the english town names model
english_town_names = fetch_list(english_towns_url)
english = TownLearner(english_town_names)
english.fit()


# The only page we serve
@app.route('/', methods=['GET', 'POST'])
def home():
    prompt = request.args.get('prompt')
    print(prompt)
    if prompt is None:
        placeholder = set()
    else:
        placeholder = english.generate_n_towns(pad_left(prompt))
    form = PromptForm()
    return render_template('index.html', title='Name my town', form=form, placeholder=placeholder)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)