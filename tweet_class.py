import mysql_backend
import mysql.connector
import re


class Tweet(object):
    cnx, cursor = mysql_backend.connect_db()

    # reads in list of stopwords
    with open("stopwords.txt", "r") as fin:
        stop_words = fin.readlines()

    def __init__(self, tweet):
        pass
        self.tweet = tweet
        self.keywords = []
        self.cashtags = []

        for word in self.tweet.text.split():
            word = word.lower()
            # Eliminate stopwords, urls and mentions
            if word in Tweet.stop_words or word[0] == "@" or word[0:4] == "http" \
                    or word[0:3] == "www" or word.isdigit():
                continue
            # Identify cashtags for stock symbols and add to list
            if word[0] == "$" and len(word) > 1 and word[1:3].isalpha():
                self.cashtags.append(word[1:].upper())
            # Add all non stopwords, urls, mentions and cashtags to list of words
            # currently including emojis and
            else:
                self.keywords.append(word)

        self.stored = self.store()

    def store(self):
        try:
            mysql_backend.insert_tweet(Tweet.cnx, Tweet.cursor, )
            return True
        except mysql.connector.Error:
            return False
