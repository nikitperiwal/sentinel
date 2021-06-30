import datetime
import pandas as pd
import datetime as dt
import tweepy
from concurrent.futures.thread import ThreadPoolExecutor


def request(api, search_string, start_date, end_date, tweet_no):
    """
    Request for tweets using 'GetOldTweets3' module.
    
    Parameters:
    -----------
    search    : str
        String to search for in tweets.
    start_date: datetime
        Date from which tweets are to be scraped
    end_date  : datetime
        Date until which tweets are to scraped
    tweetno   : int
        Number of tweets to scrap from the given time period
    """

    tweets = tweepy.Cursor(api.search,
                           q=search_string,
                           lang="en",
                           since=str(start_date),
                           until=str(end_date),
                           result_type='popular',
                           tweet_mode='extended').items(tweet_no)
    data = list()
    for tweet in tweets:
        data.append((
            tweet.created_at,
            "https://twitter.com/twitter/statuses/"+str(tweet.id),
            tweet.user.screen_name,
            tweet.full_text.replace('\n', ''),
            len(tweet.full_text),
            len(tweet.full_text.split()),
            tweet.favorite_count,
            tweet.retweet_count
        ))
    return data


def get_tweets(keywords, exclude_words=(), start_date='', end_date='', num_tweets=100):
    """
    Get Tweets for passed keywords from given time period.
    Increases the speed of scraping by using threads.
    
    Parameters:
    -----------
    keywords     : list
        List of words to search for.
    excludewords : list
        List of words that shouldn't be included in results.
    start_date   : datetime
        Date from which tweets are to be scraped
    end_date     : datetime
        Date until which tweets are to scraped
    num_tweets : int
        Number of tweets to scrap daily.
    """

    # Checking variable data
    assert any(keywords), "Please include a word to search for in keywords."
    assert start_date != '', "Please enter the start date."
    assert end_date != '', "Please enter the end date."

    # Converting variable type
    if isinstance(start_date, str):
        s_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
        start_date = s_date.date()
        
    if isinstance(end_date, str):
        e_date = dt.datetime.strptime(end_date, "%Y-%m-%d")
        end_date = e_date.date()
        
    if isinstance(num_tweets, str):
        num_tweets = int(num_tweets)

    search = ' OR '.join(keywords)
    for word in exclude_words:
        search += ' -'+word
        
    day = dt.timedelta(1)

    # Reading the credentials for twitter api
    with open("twitter_sentiment/twitter-creds.txt", 'r') as file:
        creds = file.read().split('\n')
        consumer_token = creds[0]
        consumer_secret = creds[1]
        access_token = creds[2]
        access_token_secret = creds[3]

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Using Threading to improve speed.
    futurelist = list()
    with ThreadPoolExecutor(max_workers=7) as executor:
        while start_date <= end_date:
            futurelist.append(executor.submit(request, api, search, start_date, start_date + day, num_tweets))
            start_date += day

    # Collecting the data from the threads
    data = list()
    for x in futurelist:
        data.extend(x.result())

    # Create a pandas dataframe to store the tweets.
    columns = ['datetime', 'tweet_url', 'username', 'text', 'char_length', 'word_length', 'likes', 'retweets']
    df = pd.DataFrame(data, columns=columns)
    df["datetime"] = pd.to_datetime(df["datetime"])

    # Removing outlier tweets.
    df = df[(df.datetime >= s_date) & (df.datetime <= (e_date+day))]
    return df


if __name__ == "__main__":
    dframe = get_tweets(keywords=['Trump'], exclude_words=[],
                        start_date='2021-06-28', end_date='2021-06-29',
                        num_tweets=10)
    print(dframe.head)
