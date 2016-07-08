import numpy as np
import tweet_class as tc


def train_network():
    # sets seed so that results are deterministic
    np.random.seed(1)
    # use for loop to create an array of positive and negative words
    tc.Tweet.words()

    # Real results, will involve manually categorizing tweets
    real_sent = np.array([])

    # Training loop
    for i in range(10000):
        pass


def sigmoid(x, deriv=False):
    if deriv is True:
        return x * (1 - x)

    return 1 / (1 + np.exp(-x))

