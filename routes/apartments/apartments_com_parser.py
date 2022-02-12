import re
from bs4 import BeautifulSoup


def listing_parser(raw):
    soup = BeautifulSoup(raw, 'html.parser')
    properties = []
    p_infos = soup.find_all(
        lambda t: t.name == 'article' and 'reinforcement' not in t['class'] and 'summaryWrapper' not in t['class'])
    for i in range(len(p_infos)):
        p_info = p_infos[i]
        title = p_info.find(['p', 'div'], class_='property-title')
        pricing = p_info.find(['p', 'span', 'div'], class_=[
                              'property-pricing', 'property-rents', 'price-range'])
        address = p_info.find(['div', 'p'], class_=['property-address'])
        beds = p_info.find(['p', 'span', 'div'], class_=[
                           'property-beds', 'bed-range'])
        img = p_info.find(['div'], class_='carouselInner')
        if (beds):
            beds = beds.text
        if (address):
            address = address['title']
        if (pricing):
            pricing = pricing.text
        if (title):
            title = title.text
        if (img):
            img_str = img.div['style'] if img.div.has_attr('style') else img.div['data-image'] if img.div.has_attr('data-image') else None
            m = re.search(r"(http[^\"]*)", img_str)
            if m:
                img = m.group(1)
            else:
                img = None

        properties.append(
            {"title": title, "pricing": pricing, 'address': address, 'beds': beds, 'img': img})

    return properties


def last_page_getter(raw):
    soup = BeautifulSoup(raw, 'html.parser')
    last_page_re = re.compile('page \d* of \d*', re.IGNORECASE)
    pagestring = soup.find(string=last_page_re)
    last_page = re.search('of (\d*)', pagestring)[1]
    return int(last_page)
