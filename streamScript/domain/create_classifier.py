import numpy as np

from sklearn.feature_extraction.text import CountVectorizer as CV
from sklearn.naive_bayes import MultinomialNB as MNB

from streamScript.domain.query_db import query_all_db, query_all_db_Tweet200, read_in_bb_file
import picklers

u"""You should interact with this file through the 'if name == main' block.
Edit the kwargs you want in order to create an pickle a classifier. This
classifier will be used to make your predictions."""


def check_city_locations(location_lat, location_lng):
    u"""Takes in lati"""
    bb_dict = read_in_bb_file()
    for city, values in bb_dict.items():
        lats = values[0]
        lngs = values[1]
        if (float(lats[0]) < float(location_lat) < float(lats[1])) and \
                (float(lngs[0]) < float(location_lng) < float(lngs[1])):
            return city


def get_most_common_city(user_city):
    u"""Takes in a dictionary of city names; returns the most frequently
    occurring city in the dict."""
    top = None
    top_num = 0
    for city, count in user_city.items():
        if count > top_num:
            top_num = count
            top = city
    return top


def build_test_matrix(history, vocab):
    u"""Takes in a list of lists, with each list containing tuples
    representing tweets from a single user, and a vocab list. Returns an X
    matrix of the test user features, a list of the user names, and a Y
    array of the labels."""
    matrix = []
    user_string = ""
    user_city = {}
    user_name = history[0][0]
    for tweet in history:
        if history[0][0] == user_name:
            user_string += tweet[1].lower()
            if history[0][2] and history[0][3]:
                actual = check_city_locations(history[0][2], history[0][3])
                if actual in user_city:
                    user_city[actual] += 1
                else:
                    user_city[actual] = 1
    matrix.append(user_string)
    if user_city:
        ret_user_city = get_most_common_city(user_city)
    else:
        ret_user_city = history[0][5]
    vec = CV(
        analyzer='word',
        vocabulary=vocab
    )
    print "Building test X, Y..."
    X = vec.fit_transform(matrix, vocab).todense()
    return X, user_name, ret_user_city


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


def build_matrix(data, n=10000):
    u"""Uses blocks of tweets from multiple users per city.
    Takes in a raw dataset and an optional parameter to limit the feature
    set to n. Defaults to 10000. Returns a tuple containing a matrix of n features,
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
    return user_matrix, user_array, n


def build_matrix_per_user(data, n=10000):
    u""" Uses blocks of tweets from single users per city.
    Takes in a raw dataset and an optional parameter to limit the feature
    set to n. Defaults to 10000. Returns a tuple containing a matrix of n features,
    a vector of labels, and a vocabulary list of the features examined."""
    user_matrix = []
    user_array = []
    for key, val in data.items():
        user_list = []
        count = 0
        user_count = 0
        # print key
        # print len(val)
        for tweet in val:
            if user_count >= 100:
                continue
            if count == 0:
                this_user = tweet[1]
                our_string = ""
            if (tweet[1] == this_user) and (count < 200):
                our_string += tweet[2].lower()
                count += 1
            elif (tweet[1] != this_user): # and len(our_string) >= 14000:
                count = 0
                user_count += 1
                user_matrix.append(our_string)
                user_array.append(key)
                user_list.append(this_user)

    return user_matrix, user_array, n


def fit_classifier(X, y):
    u"""Takes in an X matrix and a Y array of labels.
    Fits classifier"""
    mnb = MNB()
    return mnb.fit(X, y)


def check_alphas(X, y):
    u"""Takes in an X matrix and a Y array of labels.
    Checks four possible alpha values; returns the
    classifier with the highest cross-validated score."""
    best = None
    best_score = None
    alphas = [1E-4, 1E-3, 1E-2, 1E-1, 1]
    for alpha in alphas:
        mnb = MNB(alpha)
        score = np.mean(
            cross_val_score(mnb, X, y, cv=10)
        )
        if not best:
            best = mnb
            best_score = score
        elif score > best_score:
            best_score = score
    best.fit(X, y)
    return best, best_score



def get_raw_classifier(make_new_pickles=False, read_pickles=True, useTweet200=False):
    u"""Takes in keyword arguments to determine source of data. Returns a
    trained classifier."""
    if read_pickles:
        X = picklers.load_pickle('matrix_pickle')
        y = picklers.load_pickle('labels_pickle')
    else:
        if useTweet200:
            data = query_all_db_Tweet200()
            user_matrix, user_array, n = build_matrix_per_user(data)
        else:
            data = query_all_db(limit=True)
            user_matrix, user_array, n = build_matrix(data)
        X, y, vocab = vectorize(user_matrix, user_array, n)
    mnb = fit_classifier(X, y)
    picklers.write_pickle(mnb, 'classifier_pickle')
    if make_new_pickles:
            picklers.write_pickle(data, 'pickle')
            picklers.write_pickle(X, 'matrix_pickle')
            picklers.write_pickle(y, 'labels_pickle')
            picklers.write_pickle(vocab, 'vocab_pickle')
    print "returning mnb"
    return mnb

if __name__ == "__main__":
    print get_raw_classifier(make_new_pickles=True, read_pickles=False, useTweet200=True)
