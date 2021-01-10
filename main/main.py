import datetime

from history_analysis.analysis import analysis_company
from history_analysis.history import get_history_company
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
#
# if __name__ == '__main__':
#     initial_date = datetime.date(2020, 12, 28 - 5)
#     final_date = datetime.date(2020, 12, 28)
#
#     ticker = 'LMND'
#     can_days = 5
#     internal = "5m"
#
#     # stock_exchange_history = get_history_company(ticker, can_days, internal)
#
#     # for i in tickers:
#     analysis_company(ticker, initial_date, final_date)
#     # #
#     # # print("Hello word")
#     #
#     # actives_stocks = get_most_actives_stocks()
#     # losers = get_losers_stocks()
#     # gainers = get_gainers_stocks()
#     # print(gainers)
#     # get_technical_indicators(tickers, '30min')

import backtrader as bt
from backtesting.strategy import *


final_date = date.today()
initial_date = final_date - timedelta(days=7)

ticker = 'SRPT'
internal = "1m"

#Instantiate Cerebro engine
cerebro = bt.Cerebro()

#Add strategy to Cerebro
cerebro.addstrategy(MAcrossover)

stock = yf.Ticker(ticker)
dataframe = stock.history(start=initial_date.strftime("%Y-%m-%d"),
                          end=final_date.strftime("%Y-%m-%d"),
                          interval=internal)

data = bt.feeds.PandasData(dataname=dataframe)
cerebro.adddata(data)

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

    cerebro.plot()