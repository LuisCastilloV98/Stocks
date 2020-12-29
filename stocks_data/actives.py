import re
from datetime import date
from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'referer': 'https://finance.yahoo.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44'
}


def get_stock_information(row):
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    salida = [ele for ele in cols if ele]
    return [salida[0], salida[1], float(salida[3]), float(salida[4][:-1])]


def get_matching_stocks():
    """Run the main program"""
    plus = 100
    actual_count = 0
    template = 'https://finance.yahoo.com/most-active?count'+str(plus)+'=&offset={}&count='+str(plus)+''
    url = template.format(actual_count)
    articles = []

    while True:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # cards = soup.find_all('tr')

        table = soup.find('table')
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')
        if rows == []:
            break

        # extract rows
        for row in rows:
            information = get_stock_information(row)
            articles.append(information)

        # find the next page
        actual_count += plus
        url = template.format(actual_count)
        sleep(1)

    return articles


def get_most_actives_stocks():
    matching_stocks = get_matching_stocks()
    return matching_stocks
