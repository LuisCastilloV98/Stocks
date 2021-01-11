import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.absolute()) + "/../")

from datetime import date, timedelta
from backtesting.utils import add_data_to_cerebro
from backtesting.strategy import *
import backtrader as bt

final_date = date.today()
initial_date = final_date - timedelta(days=7)

ticker = 'AMZN'
internal = "1m"
strategy = MAcrossover

# Instantiate Cerebro engine
cerebro = bt.Cerebro()

# Add strategy to Cerebro
cerebro.addstrategy(strategy)

# Add data to Cerebro
add_data_to_cerebro(cerebro, ticker, internal, initial_date, final_date)

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
