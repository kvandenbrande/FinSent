import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import mysql_backend
import re


class Listener(StreamListener):
    def __init__(self):
        StreamListener.__init__(self)
        self.cnx, self.cursor = mysql_backend.connect_db()


    def on_data(self, data):
        try:
            mysql_backend.insert_tweet(self.cnx, self.cursor,
                                       data.user.encoding("utf-8"),
                                       data.user.time("utf-8"),
                                       data.text.encoding("utf-8"),
                                       data.text)
            return True
        except ConnectionError:
            # Create better error catching and loggin
            pass

        return True

    def on_error(self, status_code):
        pass
        return True

    def get_stocks(self):



def twitter_streaming(ticker, count):
    # Connect to twitter API
    # Variables needed to gain access to API
    count = int(count)

    consumer_key = "AyOYzIh3E2FZkIzDj19tOhD7d"
    consumer_secret = "CwR67H27PC6nOmEVRN4AOyLgKM0JJVLqqgceNOFSXt7EAB5LfP"
    access_token_key = "750911805736837120-F7OOK2eFgEjamfAzWwOIWuSudwJl9rf"
    access_token_secret = "zYJr4tUhxCRwAMDrINRUFMYyiVkRLKhPljMRtvVYtX150"
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    api = tweepy.API

    # Returns {count} most recent tweets with ticker {ticker}
    search = api.GetSearch(term=ticker, lang="en", result_type="recent", count=count)

    # parse tweets
    cleaned_tweets = []
    for tweet in search:
        cleaned_tweets.append(clean_tweet(tweet.text.encode("utf-8")))
    return cleaned_tweets


def clean_tweet(tweet_text):
    return re.sub(r"(?:\@|https?\://)\S+", "", str(tweet_text))




