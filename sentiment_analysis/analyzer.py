import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
#nltk.download('vader_lexicon')
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.absolute()) + "/../")
from sentiment_analysis.finviz import get_df_history_finviz
from sentiment_analysis.google_news import get_df_history_google_news
from sentiment_analysis.yahoo_news import get_df_history_yahoo_news


def analyzer_news_company(ticker, initial_date, final_date):
    df = get_df_history_finviz(ticker, initial_date, final_date)
    # var1_df = get_df_history_google_news(ticker, initial_date, final_date)
    # var2_df = get_df_history_yahoo_news(ticker, initial_date, final_date)
    # df = pd.concat([df, var2_df], ignore_index=True)

    # df.drop_duplicates(subset=['title'])
    # print(len(df.index))

    # sentiment analysis
    vader = SentimentIntensityAnalyzer()

    f = lambda title: vader.polarity_scores(title)['compound']
    df['compound'] = df['title'].apply(f)

    return df
