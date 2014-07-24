import numpy as np

from sklearn.feature_extraction.text import CountVectorizer as CV
from sklearn.naive_bayes import MultinomialNB as MNB

from streamScript.domain.send_data import query_all_db, query_all_db_Tweet200
import picklers

u"""Generates a vocabulary
set and builds a feature matrix. Creates a classifier and returns
cross-validated predictions. Pickles dataset and matrix as necessary."""


def build_test_matrix(user_data, vocab):
    u"""Takes in a list of lists, with each list containing tuples
    representing tweets from a single user, and a vocab list. Returns an X
    matrix of the test user features, a list of the user names, and a Y
    array of the labels."""
    matrix = []
    user_array = []
    user_cities = []
    #print user_data
    for history in user_data:
        #print history
        user_string = ""
        user_name = history[0][0]
        user_array.append(user_name)
        user_cities.append(history[0][5])
        for tweet in history:
            if history[0][0] == user_name:
                user_string += tweet[1].lower()
        matrix.append(user_string)
    vec = CV(
        analyzer='word',
        vocabulary=vocab
    )
    print "Building test X, Y..."
    X = vec.fit_transform(matrix, vocab).todense()
    # print X
    # print user_array
    # print user_cities
    return X, user_array, user_cities


def vectorize(user_matrix, user_array, n):
    stopwords = open('text/stopwords.txt').read().lower().split()
    vec = CV(
        analyzer='word',
        stop_words=stopwords,
        max_features=n,
    )
    print "Building X, Y..."
    X = vec.fit_transform(user_matrix).toarray()
    Y = np.array(user_array)
    return X, Y, vec.get_feature_names()


def build_matrix(data, n=1000):
    u"""Uses blocks of tweets from multiple users per city.
    Takes in a raw dataset and an optional parameter to limit the feature
    set to n. Defaults to 1000. Returns a tuple containing a matrix of n features,
    a vector of labels, and a vocabulary list of the features examined."""
    user_matrix = []
    user_array = []
    tweet_count = 0
    for key, val in data.items():
        for tweet in val:
            if not tweet_count % 200:
                user_array.append(key)
                user_matrix.append(" ")
            user_matrix[-1] += tweet[2].lower()
            tweet_count += 1
    return vectorize(user_matrix, user_array, n)


def build_matrix_per_user(data, n=1000):
    u""" Uses blocks of tweets from single users per city.
    Takes in a raw dataset and an optional parameter to limit the feature
    set to n. Defaults to 1000. Returns a tuple containing a matrix of n features,
    a vector of labels, and a vocabulary list of the features examined."""
    user_matrix = []
    user_array = []
    for key, val in data.items():
        count = 0
        for tweet in val:
            if count == 0:
                this_user = tweet[0]
                our_string = ""
            if (tweet[0] == this_user) and (count < 200):
                our_string += tweet[2].lower()
                count += 1
            elif (tweet[0] != this_user) and (len(user_matrix[-1]) >= 14000):
                count = 0
                user_matrix.append(our_string)
                user_array.append(key)
            elif tweet[0] != this_user:
                count = 0
    return vectorize(user_matrix, user_array, n)


def fit_classifier(X, y):
    u"""Takes in an X matrix and a Y array of labels.
    Fits classifier"""
    mnb = MNB()
    return mnb.fit(X, y)


def get_raw_classifier(make_new_pickles=False, read_pickles=True, useTweet200=False):
    u"""Takes in keyword arguments to determine to source of data. Returns a
    trained classifier."""
    if read_pickles:
        X = picklers.load_matrix_pickle()
        y = picklers.load_y_pickle()
        data = picklers.load_data_pickle()
    elif useTweet200:
        data = query_all_db_Tweet200()
        X, y, vocab = build_matrix_per_user(data)
    else:
        data = query_all_db(limit=True)
        X, y, vocab = build_matrix(data)
    mnb = fit_classifier(X, y)
    if make_new_pickles:
        picklers.pickle_classifier(mnb)
        if not read_pickles:
            picklers.pickle_data(data)
            picklers.pickle_matrix(X)
            picklers.pickle_labels(y)
            picklers.pickle_vocab(vocab)
    print "returning mnb"
    return mnb


def generate_predictions(userTestdata):
    u"""Takes in a list of twitter users' last 200 tweets, formatted as
    'blobs'. Returns a percent correct (if known), a list of all incorrect guesses
    (or unknown), and a list of all the city predictions."""
    mnb = picklers.load_classifier_pickle()
    vocab = picklers.load_vocab_pickle()
    X, user_array, user_cities = build_test_matrix(userTestdata, vocab)
    correct = 0
    incorrect = 0
    got_wrong = []
    all_results = []
    predictions = mnb.predict_log_proba(X)
    if len(predictions):
        for idx, prediction in enumerate(predictions):
            report = (user_array[idx], user_cities[idx], prediction)
            if user_cities[idx] == prediction:
                correct += 1
            else:
                incorrect += 1
                got_wrong.append(report)
            all_results.append(report)
        percent_right = correct / (float(correct) + incorrect)
        return percent_right, got_wrong, all_results

if __name__ == "__main__":
    print get_raw_classifier(make_new_pickles=True, read_pickles=False, useTweet200=False)
