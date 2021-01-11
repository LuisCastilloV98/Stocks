import yfinance as yf
from sklearn import linear_model


# Need to repare and complete code
def get_stock_linear_regression(ticker, can_days, internal):
    stock = yf.Ticker(ticker)

    # get stock info
    # print(stock.info)

    # get historical market data
    data = stock.history(period="{}d".format(can_days), interval=internal)
    stock.get_recommendations()

    # linear regression
    x = (data.index - data.index[0]).days.values.reshape(-1, 1)
    y = data[data.columns[3]].values

    model = linear_model.LinearRegression().fit(x, y)
    linear_model.LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
