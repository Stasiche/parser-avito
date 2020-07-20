from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup
import urllib.request
from os import system
import json
import ssl
import codecs

import pandas as pd
import datetime

import requests
import shutil

# url site for parse
# url_avito = 'https://www.avito.ru/hanty-mansiysk'
url_avito = 'https://www.avito.ru/sankt-peterburg/kvartiry/studiya_28_m_812_et._1885626809'
# url_avito = 'https://www.avito.ru/sankt-peterburg/fototehnika/plenochnye_fotoapparaty-ASgBAgICAUS~A6gX?q=пленочный+фотоаппарат'

# run script by timer
sched = BlockingScheduler()

# item item_table clearfix js-catalog-item-enum js-item-trackable   item-highlight   

# read html and send to BeautifulSoup.
def html_to_soup(link):
    try:
        # make ssl certificate (for launch on windows)
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

        with urllib.request.urlopen(link, context=gcontext) as response:
            # write html code to variable
            html = response.read()

        return BeautifulSoup(html, 'html.parser')

    except Exception as err:
        print('Error in html_to_soup')
        print(err.args)


def get_price_from_soup(soup:BeautifulSoup) -> int:
    try:
        return int(soup.find('span', 'js-item-price').text.replace(" ", ""))
    except:
        return -1


def get_description_from_soup(soup:BeautifulSoup) -> str:
    try:
        return ''.join([el.text for el in soup.find('div', 'item-description-text').children if el.name == 'p'])
    except:
        return ''


def check_for_dishwasher_in_description(description:str) -> bool:
    return 'посудом' in description


def get_info_from_ad(url: str) -> dict:
    soup = html_to_soup(url)

    description = get_description_from_soup(soup)

    info = {
        'price': get_price_from_soup(soup),
        'description': description,
        'link': url,
        'dishwasher_descr': check_for_dishwasher_in_description(description),

    }

    return info


def check_info(info: dict) -> bool:
    dishwasher_flag = check_for_dishwasher_in_description(info['description'])
    price_flag = info['price'] in range(10000, 30000)
    return dishwasher_flag and price_flag


def get_ad_list(url: str)->list:
    soup = html_to_soup(url)

    return ['https://www.avito.ru'+el.attrs['href'] for el in soup.find_all('a', 'snippet-link')]


def download_image(image_url: str, save_path: str) -> None:
    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream=True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(save_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


# url = 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam-ASgBAgICAUSSA8gQ?cd=1&rn=25934&f=ASgBAgICAkSSA8gQ8AeQUg'
# url = 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam-ASgBAgICAUSSA8gQ?cd=1&f=ASgBAQICAkSSA8gQ8AeQUgFAzAg0nKwBnqwBmFk'
# urls_list = get_ad_list(url)
#
# tmp_dict = {'price': [], 'description': [], 'link': [], 'dishwasher_descr': [],}
# for i, el in enumerate(urls_list):
#     print('{}/{}'.format(i+1, len(urls_list)))
#     info = get_info_from_ad(el)
#     for key, val in info.items():
#         tmp_dict[key].append(val)
# pd.DataFrame(tmp_dict).to_excel('results'+str(datetime.datetime.now())+'.xlsx', index=False)

# info = get_info_from_ad('https://www.avito.ru/sankt-peterburg/kvartiry/studiya_28_m_812_et._1885626809')
# print(check_info(info))

# download_image('http://45.img.avito.st/640x480/8601056445.jpg', './1.jpg')



