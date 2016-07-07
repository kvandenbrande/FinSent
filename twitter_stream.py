import twitter
import re


def twitter_streaming(ticker, count):
    # Connect to twitter API
    # Variables needed to gain access to API
    count = int(count)

    consumer_key = "AyOYzIh3E2FZkIzDj19tOhD7d"
    consumer_secret = "CwR67H27PC6nOmEVRN4AOyLgKM0JJVLqqgceNOFSXt7EAB5LfP"
    access_token_key = "750911805736837120-F7OOK2eFgEjamfAzWwOIWuSudwJl9rf"
    access_token_secret = "zYJr4tUhxCRwAMDrINRUFMYyiVkRLKhPljMRtvVYtX150"
    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)

    # Returns {count} most recent tweets with ticker {ticker}
    search = api.GetSearch(term=ticker, lang="en", result_type="recent", count=count)

    # parse tweets
    cleaned_tweets = []
    for tweet in search:
        cleaned_tweets.append(clean_tweet(tweet.text.encode("utf-8")))
    return cleaned_tweets


def clean_tweet(tweet_text):
    return re.sub(r"(?:\@|https?\://)\S+", "", str(tweet_text))




