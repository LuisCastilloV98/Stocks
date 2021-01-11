
import datetime
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import date, timedelta
from sklearn import linear_model
import matplotlib.pyplot as plt

import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.absolute()) + "/../")
from pytrends.request import TrendReq
from history_analysis.analysis import analysis_company
from history_analysis.history import get_history_company
from stocks_data.actives import get_most_actives_stocks
from stocks_data.gainers import get_gainers_stocks
from stocks_data.losers import get_losers_stocks
from stocks_data.techindicators import get_technical_indicators
from backtesting.strategy import *
import backtrader as bt
from sentiment_analysis.analyzer import analyzer_news_company

def fit_sentiment_days(sentiment_analysis, data):
    data['datatime'] = data.index
    list_data = data.values.tolist()
    list_data = sorted(list_data, key=lambda a: a[-1])

    list_sentiment_analysis = sentiment_analysis.values.tolist()
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

            while list_sentiment_analysis[actual_pos_sentiment+1][1] < i[-1]:
                temp_list.append(
                    list_sentiment_analysis[actual_pos_sentiment][-1])
                actual_pos_sentiment += 1
            result.append(
                [i[-1], float(sum(temp_list)) / float(len(temp_list))])

    df = pd.DataFrame(result, index=[i[0] for i in result],
                      columns=['DateTime', 'Average_news'])

    return df


pytrend = TrendReq()
kw_list = ["amazon"]
pytrend.build_payload(kw_list, cat=7, timeframe='now 7-d',
                      geo='', gprop='news')

final_date = date.today()
initial_date = final_date - timedelta(days=7)

ticker = 'AMZN'
internal = "1m"
strategy = BtcSentiment

# Instantiate Cerebro engine
cerebro = bt.Cerebro()

# Add strategy to Cerebro
cerebro.addstrategy(strategy)

stock = yf.Ticker(ticker)
dataframe = stock.history(start=initial_date.strftime("%Y-%m-%d"),
                          end=final_date.strftime("%Y-%m-%d"),
                          interval=internal)

data = bt.feeds.PandasData(dataname=dataframe)

cerebro.adddata(data)

if(strategy is BtcSentiment):
    # Second data feed
    data_trends = pytrend.interest_over_time()
    data_trends['Date'] = data_trends.index
    del data_trends["isPartial"]
    var = data_trends[data_trends.columns[0]]
    del data_trends[data_trends.columns[0]]
    data_trends['Company'] = var
    
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



stock = yf.Ticker(ticker)
dataframe = stock.history(start=initial_date.strftime("%Y-%m-%d"),
                          end=final_date.strftime("%Y-%m-%d"),
                          interval=internal)

data = bt.feeds.PandasData(dataname=dataframe)

#
sentiment_analysis_news = analyzer_news_company(ticker, initial_date, final_date)
data_news = fit_sentiment_days(sentiment_analysis_news, dataframe)
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

# Default position size
cerebro.addsizer(bt.sizers.SizerFix, stake=3)

if __name__ == '__main__':
    # Run Cerebro Engine
    start_portfolio_value = cerebro.broker.getvalue()

    cerebro.run()

    end_portfolio_value = cerebro.broker.getvalue()
    pnl = end_portfolio_value - start_portfolio_value
    print(f'Starting Portfolio Value: {start_portfolio_value:2f}')
    print(f'Final Portfolio Value: {end_portfolio_value:2f}')
    print(f'PnL: {pnl:.2f}')

    cerebro.plot(volume=False)
