import cPickle


def write_pickle(item, item_name, test=False):
    print "Pickling %s..." % item_name
    if not test:
        pickle_file = open('pickles/%s' % item_name, 'wb')
    else:
        pickle_file = open('pickles/test_%s' % item_name, 'wb')
    cPickle.dump(item, pickle_file)
    pickle_file.close()
    print "Pickled %s." % item_name


def load_pickle(item_name, test=False):
    if not test:
        pickle_file = open('pickles/%s' % str(item_name), 'rb')
    else:
        pickle_file = open('pickles/test_%s' % str(item_name), 'rb')
    print "Loading ", item_name, " pickle..."
    X = cPickle.load(pickle_file)
    print "Pickle loaded."
    pickle_file.close()
    return X
