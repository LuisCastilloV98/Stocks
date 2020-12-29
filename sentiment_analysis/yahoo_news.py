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
    'referer': 'https://www.google.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44'
}


def get_article(card):
    """Extract article information from the raw html"""
    headline = card.find('h4', 's-title').text
    source = card.find("span", 's-source').text
    posted = card.find('span', 's-time').text.replace('·', '').strip()
    description = card.find('p', 's-desc').text.strip()
    raw_link = card.find('a').get('href')
    unquoted_link = requests.utils.unquote(raw_link)
    pattern = re.compile(r'RU=(.+)\/RK')
    clean_link = re.search(pattern, unquoted_link).group(1)

    article = (headline, source, posted, description, clean_link)
    return article


def get_the_news(search):
    """Run the main program"""
    template = 'https://news.search.yahoo.com/search?p={}'
    url = template.format(search)
    articles = []
    links = set()

    while True:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', 'NewsArticle')

        # extract articles from page
        for card in cards:
            article = get_article(card)
            link = article[-1]
            if not link in links:
                links.add(link)
                articles.append(article)

                # find the next page
        try:
            url = soup.find('a', 'next').get('href')
            sleep(1)
        except AttributeError:
            break

        break

    return articles


def get_date(days_ago):
    today = date.today()

    if days_ago.find('hours'):
        today = today
    elif days_ago.find('1'):
        today -= 1
    elif days_ago.find('2'):
        today -= 2
    elif days_ago.find('3'):
        today -= 3
    elif days_ago.find('4'):
        today -= 4
    elif days_ago.find('5'):
        today -= 5
    elif days_ago.find('6'):
        today -= 6
    elif days_ago.find('7'):
        today -= 7
    elif days_ago.find('8'):
        today -= 8

    return today.strftime("%b-%d-%Y")


def get_df_history_yahoo_news(ticker, initial_date, final_date, add_stock=False):
    # run the main program
    if add_stock:
        articles = get_the_news(ticker)
    else:
        articles = get_the_news(ticker + ' stock')

    # Parse data
    parsed_data = []

    for row in articles:
        parsed_data.append([ticker,
                            get_date(row[2]),
                            '0:0:0',
                            row[0] + '. ' + row[3]])

    df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])

    df['date'] = pd.to_datetime(df.date).dt.date

    df = df[(df.date >= initial_date) & (final_date >= df.date)]

    return df
