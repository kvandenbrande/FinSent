from twitter_stream import *


def main():
    count = input("Enter the number of tweets to fetch: ")
    ticker = input("Enter the ticker of the tweets to fetch: ")

    # converts count to int type, if conversion fails, sets count to default value of 1000
    try:
        count = int(count)
    except ValueError:
        # default value
        count = 1000

    # inserts cashtag $ symbol if not already there
    if ticker[0] != "$":
        ticker = "$" + ticker

    tweets = twitter_streaming(ticker, count)

    with open("testoutput_20160706.txt", "w") as fout:
        for tweet in tweets:
            print(tweet, file=fout)

if __name__ == "__main__":
    main()
