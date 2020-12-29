from alpha_vantage.techindicators import TechIndicators


def get_technical_indicators(symbol, interval):
    ti = TechIndicators(key='S6RYSVSC0KIW03SU', output_format='pandas')
    pton_ad, q = ti.get_ad(symbol=symbol, interval=interval)

    print('Hola mundo')
