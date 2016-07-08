import mysql_backend
import mysql.connector


class Tweet(Object):
    cnx, cursor = mysql_backend.connect_db()

    def __init__(self, data):
        pass
        self.words =
        self.stored = self.store(self)


    def store(self):
        try:
            mysql_backend.insert_tweet(Tweet.cnx, Tweet.cursor, )
            return True
        except mysql.connector.Error:
            return False

    def extract_kwords(self):
        # extract keywords from text of tweet and put in list
        pass