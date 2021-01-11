from datetime import datetime
import pandas as pd
import pytz
import yfinance as yf
import backtrader as bt
from pytrends.request import TrendReq
from sentiment_analysis.analyzer import analyzer_news_company


def fit_sentiment_days(data_frame_sentiment_news, data_frame_history):
    data_frame_history['datatime'] = data_frame_history.index
    list_data = data_frame_history.values.tolist()
    list_data = sorted(list_data, key=lambda a: a[-1])

    list_sentiment_analysis = data_frame_sentiment_news.values.tolist()
    list_sentiment_analysis = sorted(
        list_sentiment_analysis, key=lambda a: a[1])

    result = []
    actual_pos_sentiment = 0
    actual_date = datetime.date(list_data[0][-1])
    temp_list = [0]
    for i in list_data:

        if actual_date < datetime.date(i[-1]):
            actual_date = datetime.date(i[-1])
            temp_list = [0]

        if list_sentiment_analysis[actual_pos_sentiment][1] > i[-1]:
            result.append(
                [i[-1], float(sum(temp_list)) / float(len(temp_list))])
        else:
            if temp_list == [0]:
                temp_list = [list_sentiment_analysis[actual_pos_sentiment][-1]]
            else:
                temp_list.append(
                    list_sentiment_analysis[actual_pos_sentiment][-1])
            actual_pos_sentiment += 1

            while list_sentiment_analysis[actual_pos_sentiment + 1][1] < i[-1]:
                temp_list.append(
                    list_sentiment_analysis[actual_pos_sentiment][-1])
                actual_pos_sentiment += 1
            result.append(
                [i[-1], float(sum(temp_list)) / float(len(temp_list))])

    df = pd.DataFrame(result, index=[i[0] for i in result],
                      columns=['DateTime', 'Average_news'])

    return df


def fit_trends_days(data_trends, data_frame_history):
    data_frame_history['datatime'] = data_frame_history.index
    list_data = data_frame_history.values.tolist()
    list_data = sorted(list_data, key=lambda a: a[-1])

    list_trend = data_trends.values.tolist()
    list_trend = sorted(list_trend, key=lambda a: a[0])

    result = []
    actual_pos_sentiment = 0
    temp_val = list_trend[0][1]
    for i in list_data:

        if list_trend[actual_pos_sentiment][0] > i[-1]:
            result.append(
                [i[-1], temp_val])
        else:
            temp_val = list_trend[actual_pos_sentiment][1]
            actual_pos_sentiment += 1

            while list_trend[actual_pos_sentiment + 1][0] < i[-1]:
                temp_val = list_trend[actual_pos_sentiment][1]
                actual_pos_sentiment += 1
            result.append(
                [i[-1], temp_val])

    df = pd.DataFrame(result, index=[i[0] for i in result],
                      columns=['DateTime', 'Company'])

    return df


def add_data_to_cerebro(cerebro, ticker, internal, initial_date, final_date):
    # Add history data to cerebro
    stock_yf = yf.Ticker(ticker)
    data_frame_history = stock_yf.history(
        start=initial_date.strftime("%Y-%m-%d"),
        end=final_date.strftime("%Y-%m-%d"),
        interval=internal)
    data_history_f = bt.feeds.PandasData(dataname=data_frame_history)

    cerebro.adddata(data_history_f)

    # Add data from google trends
    py_trend = TrendReq(hl='en-US', tz=-360)
    # kw_list = ["amazon"]
    kw_list = [ticker]
    py_trend.build_payload(kw_list, cat=7, timeframe='now 7-d',
                           geo='', gprop='news')
    data_trends = py_trend.interest_over_time()
    index = data_trends.index
    cet = pytz.timezone('America/Costa_Rica')
    data_trends.index = index.tz_localize(pytz.utc).tz_convert(cet)
    data_trends['Date'] = data_trends.index
    del data_trends["isPartial"]
    var = data_trends[data_trends.columns[0]]
    del data_trends[data_trends.columns[0]]
    data_trends['Company'] = var

    # data_trends = fit_trends_days(data_trends, data_frame_history)

    data_trends_f = bt.feeds.PandasData(
        dataname=data_trends,
        fromdate=initial_date,
        todate=final_date,
        datetime=0,
        high=-1,
        low=-1,
        open=-1,
        close=1,
        openinterest=-1,
        timeframe=bt.TimeFrame.Days)

    cerebro.adddata(data_trends_f)

    # Add data from sentiment news
    data_frame_sentiment_news = analyzer_news_company(ticker, initial_date, final_date)
    data_news = fit_sentiment_days(data_frame_sentiment_news, data_frame_history)
    data_news_f = bt.feeds.PandasData(
        dataname=data_news,
        fromdate=initial_date,
        todate=final_date,
        datetime=0,
        high=-1,
        low=-1,
        open=-1,
        close=1,
        openinterest=-1)

    cerebro.adddata(data_news_f)

    # Return cerebro

    return cerebro
