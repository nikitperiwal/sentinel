from .gettweets import get_tweets
from .classifier import predict
import pandas as pd


class TweetClass:
    def __init__(self):
        self.meta_data = None
        self.tweet_df = pd.DataFrame()
        self.context = dict()

    def scrape_tweets(self, keywords, exclude, start_date, end_date, num_tweets):
        new_meta = {
            'keywords': keywords,
            'exclude': exclude,
            'start_date': start_date,
            'end_date': end_date,
            'num_tweets': num_tweets,
        }
        if self.meta_data != new_meta:
            keywords = keywords.split()
            exclude = exclude.split()
            self.tweet_df = get_tweets(keywords, exclude, start_date, end_date, num_tweets)
            self.__classify_sentiment()
            self.meta_data = new_meta

    def __classify_sentiment(self):
        self.tweet_df['sentiment'] = predict(self.tweet_df['text'])
        
    def get_sentiment_count(self):
        sentiment_count = list(self.tweet_df.sentiment.value_counts())
        return sentiment_count
    
    def get_timeline_data(self):
        group_data = self.tweet_df.groupby(pd.Grouper(key="datetime", freq='6h'))[["sentiment"]]
        sentimentdata = group_data.mean()
        volumedata = list(group_data.size())
        indexdata = list(sentimentdata.index.strftime('%Y-%m-%dT%H:%M:%S'))
        short_sentiment = list(sentimentdata.ewm(span=3).mean().round(2).sentiment)
        long_sentiment = list(sentimentdata.ewm(span=7).mean().round(2).sentiment)
        
        return pd.DataFrame({
            'datetime'       : indexdata,
            'short_sentiment': short_sentiment,
            'long_sentiment' : long_sentiment,
            'volume'         : volumedata,
        })
    
    
    
    def get_context(self):
        if len(self.tweet_df) == 0:
            return self.context
        self.context['bar_data'] = self.get_sentiment_count()
        self.context['bar_data'].append(sum(self.context['bar_data']))
        self.context['pie_data'] = self.get_sentiment_count()
        self.context['timeseries_data'] = self.get_timeline_data()
        return self.context
    


"""
Time series:
-------------
sentiment with volume: line and bar

histogram:
------------
word length
char length
likes
comments
retweets

bar distribution:
------------------
mentions
hashtags
words
"""