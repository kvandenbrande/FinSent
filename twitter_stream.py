from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import time
import sys
import mysql_backend


class Listener(StreamListener):
    # def __init__(self):
    #     StreamListener.__init__(self)
    #     # self.cnx, self.cursor = mysql_backend.connect_db()

    def on_data(self, data):
        # try:
            # mysql_backend.insert_tweet(self.cnx, self.cursor,
            #                            data.user.encoding("utf-8"),
            #                            data.user.time("utf-8"),
            #                            data.text.encoding("utf-8"),
            #                            data.text)
        data = json.loads(data)
        # filter out retweets because they're duplicates
        try:
            if data["text"][0:2] != "RT":
                print("\n" + data["text"])
            return True
        except KeyError:
            return True

        #except ConnectionError:
            # Create better error catching and logging
         #   pass

        # return True

    def on_error(self, status_code):
        print(status_code)
        return False

    def on_timeout(self):
        time.sleep(30)
        return


def twitter_streaming(track):
    # Connect to twitter API
    # Variables needed to gain access to API
    consumer_key = "AyOYzIh3E2FZkIzDj19tOhD7d"
    consumer_secret = "CwR67H27PC6nOmEVRN4AOyLgKM0JJVLqqgceNOFSXt7EAB5LfP"
    access_token_key = "750911805736837120-F7OOK2eFgEjamfAzWwOIWuSudwJl9rf"
    access_token_secret = "zYJr4tUhxCRwAMDrINRUFMYyiVkRLKhPljMRtvVYtX150"
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    stream = Stream(auth, Listener())
    stream.filter(track=track, languages=["en"])


if __name__ == "__main__":
    stock_symbols = []

    with open("S&P500 constituents.csv", "r") as fin:
        for line in fin.readlines():
            for index, column in enumerate(line.split(",")):
                if index == 0:
                    stock_symbols.append("$" + column)

    first_half = stock_symbols[:(len(stock_symbols) // 2)]
    second_half = stock_symbols[(len(stock_symbols) // 2):]

    twitter_streaming(stock_symbols[:400])






