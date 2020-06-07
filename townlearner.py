import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


def list_as_string(l: list):
    """Simple lambda converts lists to strings"""
    s = ""
    for e in l:
        if e is not "1":
            s += e

    return s


class TownLearner:
    def __init__(self, towns, clf = RandomForestClassifier()):
        self.towns_list = towns
        self.clf = clf
        self.is_trained = False

    def create_training_data(self, towns: list) -> list:
        train = []

        for town in towns:
            #  For each word we populate the first, first two, and first three letters in to the training data
            train.append((town[0], "1", "1", "1"))  # 1s indicate placeholder letters before words start
            train.append((town[1], town[0], "1", "1"))
            train.append((town[2], town[1], town[0], "1"))

            # Then we continue sliding through the word recording the letter as the target and the
            # three preceeding letters as features
            for i in range(len(town) - 3):
                train.append((town[i + 3], town[i], town[i + 1], town[i + 2]))

            # Finally we record how the word ends in the training data
            train.append(("2", town[-3], town[-2], town[-1]))  #2s represent words terminating

        cols = ["target", "minus3", "minus2", "minus1"]
        self.train_data = pd.DataFrame(np.array(train), columns=cols)

        # Encode the letters as integers
        self.le = LabelEncoder()
        self.le.fit(pd.concat([
            self.train_data["target"],
            self.train_data["minus3"],
            self.train_data["minus2"],
            self.train_data["minus1"],
        ]))
        for col in cols:
            self.train_data[col] = self.le.transform(self.train_data[col])

    def fit(self):
        self.create_training_data(self.towns_list)
        self.clf.fit(self.train_data[["minus3", "minus2", "minus1"]], self.train_data["target"])
        self.is_trained = True

    def generate_n_towns(self, prompt, n=10, probabilistic=True, creativity=2):
        if not self.is_trained:
            raise RuntimeError("Has not been trained")

        new_towns = set()

        while len(new_towns) < n:
            continue_iterating = True
            s = self.le.transform(np.array([letter for letter in prompt])).tolist()  # TO DO - np not req'd

            while continue_iterating:
                if probabilistic:
                    probabilities = self.clf.predict_proba(np.array(s[-3:]).reshape(1, -1))[0] ** (3 / creativity)
                    new_prediction = np.random.choice(self.clf.classes_, p=probabilities / sum(probabilities))
                else:
                    new_prediction = self.clf.predict(np.array(s[-3:]).reshape(1, -1))[0]

                # If the prediction is we should terminate, we step out of iteration
                if self.le.inverse_transform([new_prediction]) == '2':
                    continue_iterating = False
                else:
                    s.append(new_prediction)

            new_town_prediction = self.le.inverse_transform(s)
            if list_as_string(new_town_prediction) not in self.towns_list:
                new_towns.add(list_as_string(new_town_prediction))

        return new_towns