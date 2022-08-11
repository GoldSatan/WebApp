import requests
from bs4 import BeautifulSoup
import random
from googletrans import Translator


# ------------------------------------------------------------------
# In this file, we actually parse the pages in the web browser.
#
# !! all variables and functions were selected specifically 
# !! for the site that was parsed, so the functionality of 
# !! this parser will not be suitable for obtaining information from other pages 
#
# ------------------------------------------------------------------

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/81.0.4196.60'
    , 'accept': '*/*'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    translator = Translator()
    newtable = []
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='content-bar')

    for item in items:
        href = item.find('a', class_='m-link-ticket').get('href')
        html = get_html(href)

        price = item.find('span', class_='bold size22 green').get_text(strip=True)


        if html.status_code == 200:

            transport = BeautifulSoup(html.text, 'html.parser')
            mileage = transport.find('div', class_='base-information bold').get_text(strip=True)
            
            if mileage == "без пробігу":
                continue
            try:
                newtable.append({
                    'title': transport.find('h1', class_='head').get_text(strip=True),
                    'type_transport': 'Autohouse',
                    'color': transport.find('span', class_='car-color').get('style').lstrip("background-color: ").removesuffix(";"),
                    'transmission': transport.find('h1', class_='transmission').get_text(strip=True),
                    'mileage': int(mileage.removesuffix("тис. км пробіг")),
                    'occasion': transport.find('h1', class_='occasion').get_text(strip=True),
                    'price': int(price.replace(" ", "")),
                    'image': transport.find('img', class_='outline m-auto').get('src'),
                    'engine': transport.find('h1', class_='engine').get_text(strip=True),
                    'note':  translator.translate(transport.find('div', class_='full-description').get_text(strip=True), dest='en').text
                })
            except:
                continue

    return newtable


def parse(URL):
    html = get_html(URL)
    if html.status_code == 200:
        cars = get_content(html.text)
        return cars
    else:
        print('Error get_html ib def parse(URL)')

def mainParse(url):
    tables = parse(url)
    return tables

if __name__ == "__main__":
    mainParse("url")
