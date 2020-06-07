import pickle
import requests
from bs4 import BeautifulSoup


def fetch_list_england(url):
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

    return filtered


english_towns_url = "https://simple.wikipedia.org/wiki/List_of_cities_and_towns_in_England"


def fetch_data_us(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")
    statelists = [state.findAll("a") for state in soup.findAll("ul", {"class": "topic-list"})]

    return [city.text for statelist in statelists for city in statelist]


us_towns_url = "https://www.britannica.com/topic/list-of-cities-and-towns-in-the-United-States-2023068"

