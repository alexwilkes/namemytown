import os
import requests
from bs4 import BeautifulSoup


main_path = os.path.dirname(os.path.abspath(__file__))


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


def drop_brackets(s):
    idx = s.find("(")
    if idx > -1:
        return s[:idx-1]


def fetch_list_germany(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")
    candidates = soup.findAll("li")  # All the cities are hyperlinks which we use to find them

    # Candidate towns are those with more than three letters
    filtered = [candidate.text for candidate in candidates if len(candidate.text) > 3]

    first = filtered.index("Aach (Baden-Württemberg)")
    last = filtered.index("Zwönitz (Saxony)")
    filtered = [drop_brackets(str(town)) for town in filtered[first:last + 1]]

    return filtered


germany_towns_url = "https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Germany"

fetch_list_germany(germany_towns_url)


def fetch_data_britannica(url, get_fresh=False):
    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")
    statelists = [state.findAll("a") for state in soup.findAll("ul", {"class": "topic-list"})]

    return [city.text for statelist in statelists for city in statelist]


us_towns_url = "https://www.britannica.com/topic/list-of-cities-and-towns-in-the-United-States-2023068"
france_towns_url = "https://www.britannica.com/topic/list-of-cities-and-towns-in-France-2039172"


def read_local_list(country):
    with open(main_path+"/townlists/"+country+".txt", "r") as fopen:
        towns = fopen.readlines()
    return towns