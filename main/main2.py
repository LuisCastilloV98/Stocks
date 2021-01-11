import datetime
from pytrends.request import TrendReq
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.absolute()) + "/../")
from history_analysis.analysis import analysis_company
from history_analysis.history import get_history_company
from sentiment_analysis.analyzer import analyzer_news_company
from stocks_data.actives import get_most_actives_stocks
from stocks_data.gainers import get_gainers_stocks
from stocks_data.losers import get_losers_stocks
from stocks_data.techindicators import get_technical_indicators
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta
from sklearn import linear_model
import matplotlib.pyplot as plt
from backtesting.strategy import *
from backtesting.utils import fit_sentiment_days
from sentiment_analysis.analyzer import *

final_date = date.today()
initial_date = final_date - timedelta(days=7)

ticker = 'TSLA'
internal = "1m"

# Instantiate Cerebro engine
cerebro = bt.Cerebro()

# Add strategy to Cerebro
cerebro.addstrategy(MAcrossover)

stock = yf.Ticker(ticker)
dataframe = stock.history(start=initial_date.strftime("%Y-%m-%d"),
                          end=final_date.strftime("%Y-%m-%d"),
                          interval=internal)

data = bt.feeds.PandasData(dataname=dataframe)

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


pytrend = TrendReq()
kw_list = ["Tesla"]
pytrend.build_payload(kw_list, cat=7, timeframe='now 7-d',
                      geo='', gprop='news')
data_trends = pytrend.interest_over_time()
data_trends['DateTime'] = data_trends.index
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
    openinterest=-1)

#Add data
cerebro.adddata(data)
cerebro.adddata(data_news_f)
cerebro.adddata(data_trends_f)



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

