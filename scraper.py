import pickle
import requests
from bs4 import BeautifulSoup


def fetch_list(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")
    candidates = soup.findAll("a")  # All the cities are hyperlinks which we use to find them

    # Candidate towns are those with more than three letters
    filtered = [candidate.text for candidate in candidates if len(candidate.text) > 3]

    # The list begins with Abingdon and ends at Yoxall so we cut the list off above and below these
    abingdon = filtered.index("Abingdon")
    yoxall = filtered.index("Yoxall")
    dropwords = ("change", "change source")  # Other hyperlinks we want to drop
    filtered = [str(town) for town in filtered[abingdon:yoxall + 1] if str(town) not in dropwords]

    print(filtered)

    return filtered


english_towns_url = "https://simple.wikipedia.org/wiki/List_of_cities_and_towns_in_England"

if __name__ == "__main__":
    with open('englishtowns.p', 'wb') as f:
        pickle.dump(fetch_list(english_towns_url), f)