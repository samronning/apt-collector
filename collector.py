import requests
from apartments_com_parser import last_page_getter


def get_all_data_by_area(location):
    responses = ""
    first_page = get_page_data_by_area(location, 1)
    last_page = last_page_getter(first_page)
    for page in range(1, last_page + 1):
        responses += (get_page_data_by_area(location, page))
    return responses


def get_page_data_by_area(location, page):
    if page is None:
        page = 1
    response = requests.get(f"https://apartments.com/{location}/{page}", headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36})"
    })
    last_page = last_page_getter(response.text)
    if int(page) > last_page:
        raise Exception("Resource not found", 404)
    return response.text
