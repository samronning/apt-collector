import re
from bs4 import BeautifulSoup


def listing_parser(raw):
    soup = BeautifulSoup(raw)
    properties = []
    p_titles = soup.find_all(class_="property-title")
    for i in range(len(p_titles)):
        properties.append(
            {"title": p_titles[i].string})

    return properties


def last_page_getter(raw):
    soup = BeautifulSoup(raw)
    last_page_re = re.compile('page \d* of \d*', re.IGNORECASE)
    pagestring = soup.find(string=last_page_re)
    last_page = re.search('of (\d*)', pagestring)[1]
    return int(last_page)
