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
            beds = re.sub("Studio", "0", beds)
            beds = re.sub(r"[^\d^-]", "", beds)
            beds = re.split("-", beds)
            if len(beds) > 1:
                bed_min = beds[0]
                bed_max = beds[1]
            else:
                bed_min = beds[0]
                bed_max = bed_min
            bed_min = int(bed_min)
            bed_max = int(bed_max)
        if (address):
            address = address['title']
        if (pricing):
            pricing = pricing.text
            if re.search(r"\d", pricing) == None:
                price_min = None
                price_max = None
            else:
                pricing = re.sub(r"[^\d^-]", "", pricing)
                pricing = re.split("-", pricing)
                if len(pricing) > 1:
                    price_min = pricing[0]
                    price_max = pricing[1]
                else:
                    price_min = pricing[0]
                    price_max = price_min
                price_min = int(price_min)
                price_max = int(price_max)
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
            {'title': title, 'price_min': price_min, 'price_max': price_max, 'address': address, 'bed_min': bed_min, 'bed_max': bed_max, 'img': img})

    return properties


def last_page_getter(raw):
    soup = BeautifulSoup(raw, 'html.parser')
    last_page_re = re.compile('page \d* of \d*', re.IGNORECASE)
    pagestring = soup.find(string=last_page_re)
    last_page = re.search('of (\d*)', pagestring)[1]
    return int(last_page)
