import numpy as np
import cPickle

from sklearn.feature_extraction.text import CountVectorizer as CV
from sklearn.naive_bayes import MultinomialNB as MNB
from sklearn.cross_validation import cross_val_score

from streamScript.domain.send_data import query_all_db

u"""Reads in a file of cities and their bounding boxes. Queries the
database to get a list of all tweets from those cities. Generates a vocabulary
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


def build_matrix(data, n=1000):
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
        max_features=n)
    print "Building X, Y..."
    X = vec.fit_transform(user_matrix).toarray()
    Y = np.array(user_array)
    print "Done"
    return X, Y, vec.get_feature_names()


def return_data_sets(make_new_pickles=False):
    try:
        pickle_file = open('pickles/pickle', 'rb')
        print "Loading Pickle..."
        data = cPickle.load(pickle_file)
        print "Pickle loaded."
        pickle_file.close()
    except IOError:
        data = query_all_db(make_new_pickles)
    return data


def return_matrix(data, make_new_pickles=False):
    u"""takes in a dataset, returns a tuple containing an X matrix of vectors
    per users, a Y array of labels, and a vocabulary list."""
    top_words = build_matrix(data, 10000)
    if make_new_pickles:
        print "Pickling..."
        pickle_file = open('pickles/xypickle', 'w')
        cPickle.dump(top_words, pickle_file)
        pickle_file.close()
        print "Pickled."
    return top_words


def fit_classifier(top_words):
    best = None
    best_score = None
    alphas = [1E-4, 1E-3, 1E-2, 1E-1, 1]
    for alpha in alphas:
        mnb = MNB(alpha)
        score = np.mean(
            cross_val_score(mnb, top_words[0], top_words[1], cv=10)
        )
        if not best:
            best = mnb
            best_score = score
        elif score > best_score:
            best_score = score
    return best, best_score


def generate_predictions():


if __name__ == "__main__":


    #our_outs = query_twitter_for_histories(data)
    #send_user_queries_to_db(our_outs)


