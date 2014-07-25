from streamScript.domain.picklers import pickle_handling
from streamScript.domain.create_classifier import check_city_locations


def test_load_pickled_classifier():
    clf = pickle_handling.load_pickle('classifier_pickle')
    assert clf.get_params()['alpha'] == 1.0
    assert clf.get_params()['fit_prior'] is True
    assert not clf.get_params()['class_prior']


def test_load_pickled_vocab():
    vocab = pickle_handling.load_pickle('vocab_pickle')
    assert len(vocab) == 10000


def test_check_city_locations():
    lat = 47.6235481
    lng = -122.33621199999999
    assert check_city_locations(lat, lng) == 'Seattle, WA'
