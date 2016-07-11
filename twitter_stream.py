from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import time
from time import strftime
import mysql_backend as mb


def twitter_streaming(track):
    # Connect to twitter API
    # Variables needed to gain access to API
    consumer_key = "CONSUMER_KEY"
    consumer_secret = "CONSUMER_SECRET"
    access_token_key = "ACCESS_TOKEN"
    access_token_secret = "ACCESS_TOKEN_SECRET"
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    stream = Stream(auth, Listener())
    stream.filter(track=track, languages=["en"])


class Listener(StreamListener):
    # def __init__(self):
    #     StreamListener.__init__(self)
    #     # self.cnx, self.cursor = mysql_backend.connect_db()
    def __init__(self):
        super().__init__()
        # self.fout = open("S&P stream.txt", "a")
        # self.fout2 = open("S&P stream full.txt", "a")
        self.error_out = open("DB import Errors.txt", "a")
        self.cnx, self.cursor = mb.connect_db()

    def on_data(self, data):
        data = json.loads(data)
        try:
            tweet_id = data["id"]
            language = data["lang"]
            tweet_time = data["timestamp_ms"]
            text = data["text"]
            stocks = data["entities"]["symbols"]
            user_screen_name = data["user"]["screen_name"]
            location = data["user"]["location"]
            follower_count = data["user"]["followers_count"]

            mb.insert_tweet(self.cnx, self.cursor,
                            tweet_id, language, tweet_time, text, stocks, user_screen_name,
                            location, follower_count)
        # try:
        #     if data["text"][0:2] != "RT":
        #         print("\n" + strftime("%Y-%m-%d %H:%M:%S") + "\n" + data["text"], file=Listener.fout)
        #         print(json.dumps(data, indent=4, sort_keys=True), file=Listener.error_out)
        #     return True
        except KeyError:
            print("Key error | " + strftime("%Y-%m-%d %H:%M:%S"))
            return
        # Certain characters like emojis aren't working properly and are causing encoding errors
        except UnicodeEncodeError:
            print("\n" + strftime("%Y-%m-%d %H:%M:%S") + "\nUnicode error", file=self.error_out)
            print("Unicode error | " + strftime("%Y-%m-%d %H:%M:%S"))
            return True
        except ConnectionError:
            print("Connection error | " + strftime("%Y-%m-%d %H:%M:%S"))
            try:
                print("\nConnection error\n" + json.dumps(data, indent=4, sort_keys=True), file=self.error_out)
            except UnicodeEncodeError:
                print("\n" + strftime("%Y-%m-%d %H:%M:%S") + "\nUnicode error", file=self.error_out)
            return True

    def on_error(self, status_code):
        print("Error status code: " + str(status_code)+ " | " + strftime("%Y-%m-%d %H:%M:%S"))
        print("\n" + strftime("%Y-%m-%d %H:%M:%S") + "\nError status code: " + str(status_code), file=self.error_out)
        return

    def on_timeout(self):
        # On Twitter connection timeout, retry in a minute
        print("Twitter connection timeout")
        print("\n" + strftime("%Y-%m-%d %H:%M:%S") + "\n""Twitter connection timeout", file=self.error_out)
        time.sleep(60)
        return


if __name__ == "__main__":
    stock_symbols = []

    with open("S&P500 constituents.csv", "r") as fin:
        for line in fin.readlines():
            for index, column in enumerate(line.split(",")):
                if index == 0:
                    stock_symbols.append("$" + column)

    twitter_streaming(stock_symbols[:400])






