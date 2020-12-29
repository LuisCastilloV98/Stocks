from urllib.request import urlopen, Request

import pandas as pd
from bs4 import BeautifulSoup


def get_df_history_finviz(ticker, initial_date, final_date):
    finviz_url = 'https://finviz.com/quote.ashx?t='

    # get html
    url = finviz_url + ticker

    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response, features='html.parser')
    news_table_html = html.find(id='news-table')

    # parse html
    parsed_data = []

    for row in news_table_html.findAll('tr'):

        title = row.a.text
        date_data = row.td.text.split(' ')

        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([ticker, date, time, title])

    df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])

    df['date'] = pd.to_datetime(df.date).dt.date

    df = df[(df.date >= initial_date) & (final_date >= df.date)]

    return df
