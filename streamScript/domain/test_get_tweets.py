import random
import cPickle
import os
# from mock import patch, Mock
# import mock
# import get_tweets_by_user
from get_tweets_by_user import get_twitter_api
from get_tweets_by_user import read_in_bb_file
from get_tweets_by_user import get_unique_handles
from get_tweets_by_user import format_tweet_history
from get_tweets_by_user import query_twitter_for_histories
from make_predictions_per_user import make_prediction
from streamScript.domain.send_data import query_db

import pytest
slow = pytest.mark.slow
pickle = pytest.mark.pickle



@pytest.fixture(scope="session")
def create_pickle(request):
    u"""Create a pickle."""
    try:
        pickle_file = open('pickles/test_tweets', 'rb')
        histories, count = cPickle.load(pickle_file)
        pickle_file.close()
    except IOError:
        bb_dict = read_in_bb_file()
        a_key = random.choice(bb_dict.keys())
        values = bb_dict[a_key]
        vals = query_db(a_key,values)
        handles = get_unique_handles(vals)
        histories = query_twitter_for_histories(handles, a_key, cap=3)
        count = 0
        pickle_file = open('pickles/test_tweets', 'wb')
        users_tweets_count = histories, count
        cPickle.dump(users_tweets_count, pickle_file)
        pickle_file.close()

    def fin():
        users_tweets_count = histories, count + 1
        print "+++++++++++"
        print count
        if count < 10:
            pickle_file = open('pickles/test_tweets', 'wb')
            cPickle.dump(users_tweets_count, pickle_file)
            pickle_file.close()
        else:
            os.remove('pickles/test_tweets')

    request.addfinalizer(fin)

    return histories


def test_get_twitter_api():
    api = get_twitter_api().next()
    assert api.host == "api.twitter.com"


def test_read_in_bb_file():
    bb_dict = read_in_bb_file()
    a = {}
    assert type(bb_dict) == type(a)
    assert len(bb_dict) != 0

@slow
def test_query_db():
    bb_dict = read_in_bb_file()
    a_key = random.choice(bb_dict.keys())
    values = bb_dict[a_key]
    vals = query_db(a_key, values)
    assert len(vals) != 0
    assert type(vals[0][0]) == type(6)
    assert type(vals[0][1]) == type(u'a')

@slow
def test_get_unique_handles():
    bb_dict = read_in_bb_file()
    a_key = random.choice(bb_dict.keys())
    values = bb_dict[a_key]
    vals = query_db(a_key, values)
    handles = get_unique_handles(vals)
    assert len(handles) != 0
    assert isinstance(handles[0], unicode)


def test_query_twitter_for_histories(create_pickle):
    u"""This test fails on occasion, specficially when a users first tweet
    doesn't have location data."""
    histories = create_pickle
    tweets = histories[0]
    tweet = tweets[0]
    print tweet
    assert len(tweet) == 7
    assert isinstance(tweet[0], unicode)


# def test_make_prediction():
#     pass

# @mock.patch('streamScript.domain.get_tweets_by_user.query_twitter_for_histories')
# def test_make_prediction(mock_query_twitter_for_histories, create_pickle):
#     mock_query_twitter_for_histories.return_value=create_pickle
#     results = make_prediction('unused')
#     assert results == "hello"



# if __name__ == '__main__':
#     test_query_twitter_for_histories()