from flask import Flask, request
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


def fetch_list(url):
    dropwords = ("change", "change source")
    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")
    candidates = soup.findAll("a")
    filtered = [candidate.text for candidate in candidates if len(candidate.text) > 3][11:]
    yoxall = filtered.index("Yoxall")
    filtered = [str(town) for town in filtered[:yoxall + 1] if str(town) not in dropwords]

    return filtered

wikipedia_url = "https://simple.wikipedia.org/wiki/List_of_cities_and_towns_in_England"
towns = fetch_list(wikipedia_url)

train = []
names = ""

for town in towns:
    train.append((town[0], "1", "1", "1"))
    train.append((town[1], town[0], "1", "1"))
    train.append((town[2], town[1], town[0], "1"))

    for i in range(len(town) - 3):
        train.append((town[i + 3], town[i], town[i + 1], town[i + 2]))

    train.append(("2", town[-3], town[-2], town[-1]))

cols = ["target", "minus3", "minus2", "minus1"]
df = pd.DataFrame(np.array(train),columns=cols)
le = LabelEncoder()
le.fit(pd.concat([df["target"], df["minus3"], df["minus2"], df["minus1"]]))
for col in cols:
    df[col] = le.transform(df[col])


X = df[["minus3", "minus2", "minus1"]]
y = df["target"]
clf = RandomForestClassifier()
clf.fit(X, y)


def list_as_string(list):
    s = ""
    for e in list:
        if e is not "1":
            s += e

    return s


def generate_n_towns(prompt, n=10, probabilistic=True, creativity=2):
    new_towns = set()
    while len(new_towns) < n:
        continue_iterating = True
        s = le.transform(np.array([letter for letter in prompt])).tolist()

        while continue_iterating:
            if probabilistic:
                probabilities = clf.predict_proba(np.array(s[-3:]).reshape(1, -1))[0] ** (3 / creativity)
                new_prediction = np.random.choice(clf.classes_, p=probabilities / sum(probabilities))
            else:
                new_prediction = clf.predict(np.array(s[-3:]).reshape(1, -1))[0]

            if le.inverse_transform([new_prediction]) == '2':
                continue_iterating = False
            else:
                s.append(new_prediction)

        if list_as_string(le.inverse_transform(s)) not in towns:
            new_towns.add(list_as_string(le.inverse_transform(s)))

    return new_towns


app = Flask(__name__)


# The only page we serve
@app.route('/')
def home():
    prompt = request.args.get('prompt')
    return str(generate_n_towns(prompt=prompt))


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)