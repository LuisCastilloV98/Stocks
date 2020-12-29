import matplotlib.pyplot as plt

from history_analysis.history import get_history_company
from sentiment_analysis.analyzer import analyzer_news_company


def analysis_company(ticker, initial_date, final_date):
    news_history = analyzer_news_company(ticker, initial_date, final_date)

    # Plot a Bar Chart
    plt.figure(figsize=(10, 8))
    mean_df = news_history.groupby(['ticker', 'date']).mean().unstack()
    mean_df = mean_df.xs('compound', axis="columns")
    mean_df.plot(kind='bar')
    plt.show()
    pass
