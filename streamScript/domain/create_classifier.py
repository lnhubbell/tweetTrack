import numpy as np
import cPickle

from get_tweets_by_user import query_db, read_in_bb_file
from sklearn.feature_extraction.text import CountVectorizer as CV
from sklearn.naive_bayes import MultinomialNB as MNB
from sklearn.cross_validation import cross_val_score


u"""Reads in a file of cities and their bounding boxes. Queries the
database to get a list of all tweets from those cities. Generates a vocabulary
set and builds a feature matrix. Creates a classifier and returns
cross-validated predictions. Pickles dataset and matrix as necessary."""


def query_all_db(new_pickle=False):
    i = 0
    bb_dict = read_in_bb_file()
    data_set = {}
    for key, values in bb_dict.items():
        data = query_db(key, values)
        data_set[key] = data
        i += 1
    if new_pickle:
        pickle_file = open('pickles/pickle', 'w')
        cPickle.dump(data_set, pickle_file)
        pickle_file.close()
        print "Created Pickle"
    return data_set


def build_vocab(data, n=1000):
    u"""MAY BE DEPRECATED Takes in a dict with locations as the keys
    and a list of tweets
    as the values. Returns a list of tuples (word, word count) for the
    top n words."""
    vocab = {}
    stopwords = open('text/stopwords.txt').read().lower().split()
    # print data
    for key, val in data.items():
        # print "++++++++++++++"
        # print "Val: " + str(val)
        for tweet in val:
            # print "Tweet:" + str(tweet)
            the_text = tweet[2]
            print the_text
            the_text = the_text.lower().split()
            # print "The Text: " + str(the_text)
            for word in the_text:
                # print "Word: " + str(word)
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
    # print user_matrix
    # print len(user_matrix)
    X = vec.fit_transform(user_matrix).toarray()
    print X
    print len(X)
    for x in X:
        print len(x)
    Y = np.array(user_array)
    print Y
    print len(Y)
    print "Done"
    return X, Y, vec.get_feature_names()

if __name__ == "__main__":
    try:
        pickle_file = open('pickles/pickle', 'rb')
        print "Loading Pickle..."
        data = cPickle.load(pickle_file)
        print "Pickle loaded."
        pickle_file.close()
    except IOError:
        data = query_all_db(True)
    top_words = build_matrix(data, 10000)
    print "Pickling..."
    pickle_file = open('pickles/xypickle', 'w')
    cPickle.dump(top_words, pickle_file)
    pickle_file.close()
    print "Pickled."

    #our_outs = query_twitter_for_histories(data)
    #send_user_queries_to_db(our_outs)

    alphas = [1E-4, 1E-3, 1E-2, 1E-1, 1]
    for alpha in alphas:
        mnb = MNB(alpha)
        print alpha, np.mean(
            cross_val_score(mnb, top_words[0], top_words[1], cv=5)
        )


    # for city, users in our_outs.items():
    #     print city, len(users)

    # for city, tweets in our_outs.items:
    #     print "\n\n", "*" * 10, "\n\n"
    #     print city, "\n\n"
    #     print len(tweets)
    #     print "\n\n", "*" * 20, "\n\n"
    # nulls = 0
    # null_keys = []
    # for key, vals in data.items():
    #     if len(vals) < 1:
    #         nulls += 1
    #         null_keys.append(key)
    # print "No values for ", nulls, " cities: ", null_keys
