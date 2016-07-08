import mysql.connector


def connect_db():
    # Connect to hosted MySQL database containining the tweet data
    try:
        db_name = "u452455758_fstwt"
        db_host = "mysql.hostinger.in"
        db_username = "u452455758_dev"
        db_password = "DeltaChi"

        cnx = mysql.connector.connect(user=db_username, password=db_password,
                                      host=db_host, database=db_name)

        cnx.autocommit = True
        cursor = cnx.cursor(buffered=True)
        return [cnx, cursor]
    except mysql.connector.Error:
        raise ConnectionError


def insert_tweet(cnx, cursor, user, time, text, stocks):
    # Insert one tweet into the database

    # Insertion query
    insert_tweet_q = "INSERT INTO tweets (tweet_id, user, tweet_time, text, stock, multi_stock)" \
                     "VALUES (null, {0}, {1}, {2}, {3}, {4});"

    # Account for tweets where more than one stock is mentioned
    if stocks is list and len(stocks) > 1:
        for stock in stocks:
            tweet_data = (user, time, text, stock, len(stocks))
            try:
                cursor.execute(insert_tweet_q, tweet_data)
            except mysql.connector.Error:
                cnx.rollback()
                break

    # Normal tweet with one stock
    else:
        # Case where stock is in list with length of 1
        if stocks is list:
            stock = stocks[0]
        else:
            stock = stocks

        tweet_data = (user, time, text, stock, 1)

        try:
            cursor.execute(insert_tweet_q, tweet_data)
        except mysql.connector.Error:
            cnx.rollback()
