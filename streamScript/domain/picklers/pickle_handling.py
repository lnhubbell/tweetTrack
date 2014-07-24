import cPickle


def load_matrix_pickle():
    pickle_file = open('pickles/matrix_pickle', 'rb')
    print "Loading matrix pickle..."
    X = cPickle.load(pickle_file)
    print "Matrix pickle loaded."
    pickle_file.close()
    return X


def load_classifier_pickle():
    pickle_file = open('pickles/classifier_pickle', 'rb')
    print "Loading classifier pickle..."
    mnb = cPickle.load(pickle_file)
    print "Classifier pickle loaded."
    pickle_file.close()
    return mnb


def load_vocab_pickle():
    pickle_file = open('pickles/vocab_pickle', 'rb')
    print "Loading vocab pickle..."
    vocab = cPickle.load(pickle_file)
    print "Vocab pickle loaded."
    pickle_file.close()
    return vocab


def load_y_pickle():
    pickle_file = open('pickles/labels_pickle', 'rb')
    print "Loading labels pickle..."
    labels = cPickle.load(pickle_file)
    print "Labels pickle loaded."
    pickle_file.close()
    return labels


def load_data_pickle():
    pickle_file = open('pickles/pickle', 'rb')
    print "Loading data pickle..."
    data = cPickle.load(pickle_file)
    print "Data pickle loaded."
    pickle_file.close()
    return data


def pickle_data(data_set):
    print "Pickling dataset..."
    pickle_file = open('pickles/pickle', 'wb')
    cPickle.dump(data_set, pickle_file)
    pickle_file.close()


def pickle_classifier(clf):
    print "Pickling classifier..."
    pickle_file = open('pickles/classifier_pickle', 'wb')
    cPickle.dump(clf, pickle_file)
    pickle_file.close()


def pickle_matrix(X):
    print "Pickling matrix..."
    pickle_file = open('pickles/matrix_pickle', 'wb')
    cPickle.dump(X, pickle_file)
    pickle_file.close()
    print "Pickled matrix"


def pickle_labels(y):
    print "Pickling labels..."
    pickle_file = open('pickles/labels_pickle', 'wb')
    cPickle.dump(y, pickle_file)
    pickle_file.close()
    print "Pickled y labels"


def pickle_vocab(vocab):
    print "Pickling vocab..."
    pickle_file = open('pickles/vocab_pickle', 'wb')
    cPickle.dump(vocab, pickle_file)
    pickle_file.close()
    print "Pickled vocab."
