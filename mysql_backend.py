import mysql.connector
import datetime as dt


def connect_db():
    # Connect to hosted MySQL database containining the tweet data
    try:
        db_name = "finsent"
        db_host = "localhost"
        db_username = "root"
        db_password = input("Please enter the database password: ")

        cnx = mysql.connector.connect(user=db_username, password=db_password,
                                      host=db_host, database=db_name)

        cnx.autocommit = True
        cursor = cnx.cursor(buffered=True)
        return [cnx, cursor]

    except mysql.connector.Error:
        raise ConnectionError


def insert_tweet(cnx, cursor, tweet_id, language, tweet_time, text,
                 stocks, user_screen_name, user_location, followers_count):
    # Format inputs
    try:
        tweet_id = int(tweet_id)
    except ValueError:
        raise ConnectionError

    tweet_time = timestamp_to_dt(tweet_time)

    # Get rid of html &amp;
    text = text.replace("&amp;", "&", 10)

    try:
        followers_count = int(followers_count)
    except ValueError:
        followers_count = None

    # Insertion query
    insert_tweet_q = "INSERT INTO tweets (entry_id, tweet_id, language, tweet_time, text, stock, " \
                     "multi_stock, user_screen_name, user_location, followers_count)" \
                     "VALUES (null, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    # Account for tweets where more than one stock is mentioned
    if type(stocks) is list and len(stocks) > 1:
        for stock in stocks:
            try:
                stock = stock["text"].upper()
            except IndexError:
                raise ConnectionError

            tweet_data = (tweet_id, language, tweet_time, text,
                          stock, len(stocks), user_screen_name, user_location, followers_count)
            try:
                cursor.execute(insert_tweet_q, tweet_data)
            except mysql.connector.Error:
                cnx.rollback()
                raise ConnectionError

    # Normal tweet with one stock
    else:
        # Case where stock is in list with length of 1
        try:
            stock = stocks[0]["text"].upper()
        except IndexError:
            raise ConnectionError

        tweet_data = (tweet_id, language, tweet_time, text,
                      stock, 1, user_screen_name, user_location, followers_count)

        try:
            cursor.execute(insert_tweet_q, tweet_data)
        except mysql.connector.Error:
            raise ConnectionError


def timestamp_to_dt(timestamp):
    try:
        # Because twitter timestamp is in milliseconds divide by 1000 to nearest whole number
        return dt.datetime.fromtimestamp(int(timestamp)//1000).strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

