import datetime

from history_analysis.analysis import analysis_company
from history_analysis.history import get_history_company
from stocks_data.actives import get_most_actives_stocks
from stocks_data.gainers import get_gainers_stocks
from stocks_data.losers import get_losers_stocks
from stocks_data.techindicators import get_technical_indicators

import matplotlib.pyplot as plt

if __name__ == '__main__':
    initial_date = datetime.date(2020, 12, 28 - 5)
    final_date = datetime.date(2020, 12, 28)

    ticker = 'LMND'
    can_days = 5
    internal = "5m"

    # stock_exchange_history = get_history_company(ticker, can_days, internal)

    # for i in tickers:
    analysis_company(ticker, initial_date, final_date)
    # #
    # # print("Hello word")
    #
    # actives_stocks = get_most_actives_stocks()
    # losers = get_losers_stocks()
    # gainers = get_gainers_stocks()
    # print(gainers)
    # get_technical_indicators(tickers, '30min')
