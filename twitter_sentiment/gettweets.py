import pandas as pd
import datetime as dt
import snscrape.modules.twitter as sntwitter
from concurrent.futures.thread import ThreadPoolExecutor


def request(search, start_date, end_date, tweet_no):
    """
    Request for tweets using 'SNScrape' module.
    
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

    search += f" since:{str(start_date)}"
    search += f" until:{str(end_date)}"
    search += f" lang:en"
    
    tweets = sntwitter.TwitterSearchScraper(search).get_items()
    
    data = []
    for i, tweet in enumerate(tweets):
        data.append((str(tweet.date)[:-6],
                    tweet.url,
                    tweet.user.username,
                    tweet.content,
                    len(tweet.content),
                    len(tweet.content.split()),
                    tweet.likeCount,
                    tweet.replyCount,
                    tweet.retweetCount,))
        if i>tweet_no:
            break
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
    assert any(keywords), "Please include a word to search for in keywords"
    assert start_date != '', "Please enter the start date"
    assert end_date != '', "Please enter the end date"

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
    with ThreadPoolExecutor(max_workers=7) as executor:
        while start_date <= end_date:
            futurelist.append(executor.submit(request, search, start_date, start_date + day, num_tweets))
            start_date += day

    # Collecting the data from the threads
    data = list()
    for x in futurelist:
        data.extend(x.result())

    # Create a pandas dataframe to store the tweets.
    columns = ['datetime', 'tweet_url', 'username', 'text', 'char_length', 'word_length', 'likes', 'replies', 'retweets']
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
