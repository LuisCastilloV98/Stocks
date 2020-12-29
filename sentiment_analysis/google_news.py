import datetime

import pandas as pd
from GoogleNews import GoogleNews


def get_df_history_google_news(ticker, initial_date, final_date, add_stock=False):
    googlenews = GoogleNews(lang='en',
                            start=datetime.date.strftime(initial_date, "%m/%d/%Y"),
                            end=datetime.date.strftime(final_date, "%m/%d/%Y"),
                            encode='utf-8')
    if add_stock:
        googlenews.get_news(ticker + ' stock')
        # googlenews.search(ticker + ' stock')
    else:
        googlenews.get_news(ticker)
        # googlenews.search(ticker)

    result = googlenews.results()

    # parse data
    parsed_data = []

    for row in result:
        title = row['title'] + ". " + row['desc']
        date = row['datetime'].strftime("%b-%d-%Y")
        time = row['datetime']

        parsed_data.append([ticker, date, time, title])

    df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])

    df['date'] = pd.to_datetime(df.date).dt.date

    df = df[(df.date >= initial_date) & (final_date >= df.date)]

    return df
