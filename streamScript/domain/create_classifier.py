import numpy as np
import cPickle

from sklearn.feature_extraction.text import CountVectorizer as CV
from sklearn.naive_bayes import MultinomialNB as MNB
from sklearn.cross_validation import cross_val_score

from streamScript.domain.send_data import query_all_db

u"""Generates a vocabulary
set and builds a feature matrix. Creates a classifier and returns
cross-validated predictions. Pickles dataset and matrix as necessary."""


def build_vocab(data, n=1000):
    u"""MAY BE DEPRECATED Takes in a dict with locations as the keys
    and a list of tweets
    as the values. Returns a list of tuples (word, word count) for the
    top n words."""
    vocab = {}
    stopwords = open('text/stopwords.txt').read().lower().split()
    for key, val in data.items():
        for tweet in val:
            the_text = tweet[2]
            print the_text
            the_text = the_text.lower().split()
            for word in the_text:
                if word not in stopwords:
                    vocab[word] = vocab.setdefault(word, 0) + 1
    the_list = sorted(vocab.items(), key=lambda x: -x[1])
    return the_list[:n]


def build_test_matrix(user_data, vocab):
    u"""Takes in a list of lists, with each list containing tuples
    representing tweets from a single user, and a vocab list. Returns an X
    matrix of the test user features, a list of the user names, and a Y
    array of the labels."""
    user_matrix = []
    user_array = []
    user_cities = []
    for history in user_data:
        user_name = history[0][0]
        user_array.append(user_name)
        user_cities.append(history[0][5])
        for tweet in history:
            if history[0][0] == user_name:
                user_matrix.append(" ")
            user_matrix[-1] += tweet[2].lower()
    vec = CV(
        analyzer='word',
        vocabulary=vocab
    )
    print "Building test X, Y..."
    X = vec.fit_transform(user_matrix, vocab).toarray()
    return X, user_array, user_cities


def build_matrix(data, n=1000):
    u"""Takes in a raw dataset and an optional parameter to limit the feature
    set to n. Defaults to 1000. Returns a tuple containing a matrix of n features,
    a vector of labels, and a vocabulary list of the features examined."""
    stopwords = open('text/stopwords.txt').read().lower().split()
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
    vec = CV(
        analyzer='word',
        stop_words=stopwords,
        max_features=n,
    )
    print "Building X, Y..."
    X = vec.fit_transform(user_matrix).toarray()
    Y = np.array(user_array)
    print "Done"
    return X, Y, vec.get_feature_names()


def return_data_sets(read_pickle=False, make_new_pickles=False):
    u"""Takes in two optional keyword arguments; will either read in
    a dataset from disk or will call a function to query the DB to generate
    a new dataset. If a 'make_new_pickles' keyword arg set to True is passed,
    the DB function will make a new pickle for future use. Returns a
    raw dataset."""
    if read_pickle:
        try:
            pickle_file = open('pickles/pickle', 'rb')
            print "Loading data pickle..."
            data = cPickle.load(pickle_file)
            print "Data pickle loaded."
            pickle_file.close()
        except IOError as err:
            return "Cannot read from existing pickle.", err.message
    elif make_new_pickles:
        data = query_all_db(make_new_pickles)
    else:
        data = query_all_db()
    return data


def return_matrix(data, make_new_pickles=False):
    u"""takes in a dataset, returns a tuple containing an X matrix of vectors
    per users, a Y array of labels, and a vocabulary list."""
    top_words = build_matrix(data, 10000)
    if make_new_pickles:
        print "Pickling X, y, vocab..."
        pickle_file = open('pickles/xypickle', 'wb')
        cPickle.dump(top_words, pickle_file)
        pickle_file.close()
        print "Pickled X, y, vocab."
    return top_words


def fit_classifier(X, y):
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
    return best, best_score


def get_raw_classifier(
    read_pickle=True, make_new_pickles=False, readXYpickle=True
):
    u"""Takes in keyword arguments to determine to source of data. Returns a
    trained classifier."""
    if readXYpickle:
        try:
            pickle_file = open('pickles/xypickle', 'rb')
            print "Loading X, y, vocab pickle..."
            X, y, vocab = cPickle.load(pickle_file)
            print "X, y, vocab pickle loaded."
            pickle_file.close()
        except IOError as err:
            return "Cannot read from existing pickle.", err.message
    else:
        data = return_data_sets(read_pickle, make_new_pickles)
        X, y, vocab = return_matrix(data, make_new_pickles)
        mnb, score = fit_classifier(X, y)
    if make_new_pickles:
        print "Pickling classifier..."
        pickle_file = open('pickles/classifier_pickle', 'wb')
        cPickle.dump(mnb, pickle_file)
        pickle_file.close()
        print "Pickled classifier."
    return mnb


def generate_predictions(userTestdata):
    mnb = get_raw_classifier()
    X, user_array, user_cities = build_test_matrix(userTestdata)
    correct = 0
    incorrect = 0
    got_wrong = []
    predictions = mnb.predict(X)
    for idx, prediction in predictions:
        if prediction == user_cities[idx]:
            correct += 1
        else:
            incorrect += 1
            report = (user_array[idx], user_array[idx], prediction)
            got_wrong.append(report)
    percent_right = correct / (float(correct) + incorrect)
    return percent_right, got_wrong

if __name__ == "__main__":
    print get_raw_classifier(make_new_pickles=True, read_pickle=False, readXYpickle=False)

    #our_outs = query_twitter_for_histories(data)
    #send_user_queries_to_db(our_outs)


