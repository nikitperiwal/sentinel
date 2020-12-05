from GetOldTweets3.manager import TweetCriteria, TweetManager
from concurrent.futures.thread import ThreadPoolExecutor
import pandas as pd
import datetime as dt


def request(search, start_date, end_date, tweet_no):
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

    tc = TweetCriteria()
    tc.setQuerySearch(search)
    tc.setSince(str(start_date))
    tc.setUntil(str(end_date))
    tc.setLang("en")
    tc.setTopTweets(True)
    tc.setMaxTweets(tweet_no)
    tweets = TweetManager.getTweets(tc)

    data = list()
    for tweet in tweets:
        data.append((str(tweet.date)[:19],
                     tweet.permalink,
                     tweet.username,
                     tweet.text,
                     len(tweet.text),
                     len(tweet.text.split()),
                     tweet.favorites,
                     tweet.retweets,
                     tweet.replies,
                    ))

    return data


def get_tweets(keywords=[], exclude_words=[], start_date='', end_date='', num_tweets=100):
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

    # Using Threading to improve speed.
    futurelist = list()
    with ThreadPoolExecutor(max_workers=20) as executor:
        while start_date <= end_date:
            futurelist.append(executor.submit(request, search, start_date, start_date + day, num_tweets))
            start_date += day
    data = list()
    for x in futurelist:
        data.extend(x.result())

    # Create a pandas dataframe to store the tweets.
    columns = ['datetime', 'tweet_url', 'username', 'text', 'char_length', 'word_length',
               'likes', 'retweets', 'replies']
    df = pd.DataFrame(data, columns=columns)
    df["datetime"] = pd.to_datetime(df["datetime"])

    # Removing outlier tweets.
    df = df[(df.datetime >= s_date) & (df.datetime <= (e_date+day))]
    return df


if __name__ == "__main__":
    df = get_tweets(keywords=['Mahindra'], exclude_words=[], start_date='2020-01-01', end_date='2020-01-03', num_tweets=100)
    print(df.head)
