import random
import cPickle
import os

from get_tweets_by_user import get_twitter_api
from get_tweets_by_user import read_in_bb_file
from get_tweets_by_user import get_unique_handles
from get_tweets_by_user import format_blob
from get_tweets_by_user import query_twitter_for_histories
from streamScript.domain.send_data import query_db

import pytest
slow = pytest.mark.slow
pickle = pytest.mark.pickle


@pytest.fixture(scope="session")
def create_pickle(request):
    u"""Create a pickle."""
    try:
        pickle_file = open('pickles/test_tweets', 'rb')
        users_tweets, count = cPickle.load(pickle_file)
        pickle_file.close()
    except IOError:
        bb_dict = read_in_bb_file()
        a_key = random.choice(bb_dict.keys())
        values = bb_dict[a_key]
        vals = query_db(a_key,values)
        handles = get_unique_handles(vals)
        users_tweets = query_twitter_for_histories(handles, a_key, cap=3)
        count = 0
        pickle_file = open('pickles/test_tweets', 'wb')
        users_tweets_count = users_tweets, count
        cPickle.dump(users_tweets_count, pickle_file)
        pickle_file.close()

    def fin():
        users_tweets_count = users_tweets, count + 1
        print "+++++++++++"
        print count
        if count < 50:
            pickle_file = open('pickles/test_tweets', 'wb')
            cPickle.dump(users_tweets_count, pickle_file)
            pickle_file.close()
        else:
            os.remove('pickles/test_tweets')

    request.addfinalizer(fin)

    return users_tweets


# @pytest.fixture(scope="session")
# def smtp(request):
#     def fin():
#         pickle_file = open('pickles/test_tweets', 'wb')
#         users_tweets = users_tweets, count + 1
#         print "+++++++++++"
#         print count
#         if count < 5:
#             cPickle.dump(users_tweets, pickle_file)
#             pickle_file.close()
#         else:
#             os.remove('pickles/test_tweets')

#     request.addfinalizer(fin)


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
    vals = query_db(a_key,values)
    assert len(vals) != 0
    assert type(vals[0][0]) == type(6)
    assert type(vals[0][1]) == type(u'a')

@slow
def test_get_unique_handles():
    bb_dict = read_in_bb_file()
    a_key = random.choice(bb_dict.keys())
    values = bb_dict[a_key]
    vals = query_db(a_key,values)
    handles = get_unique_handles(vals)
    assert len(handles) != 0
    assert type(handles[0]) == type(u'a')

@slow
def test_query_twitter_for_histories():
    u"""This test fails on occasion, specficially when a users first tweet
    doesn't have location data."""
    bb_dict = read_in_bb_file()
    a_key = random.choice(bb_dict.keys())
    values = bb_dict[a_key]
    vals = query_db(a_key,values)
    handles = get_unique_handles(vals)
    users_tweets = query_twitter_for_histories(handles, a_key, cap=3)
    tweets = users_tweets[0]
    tweet = tweets[0]
    print tweet
    assert len(tweet) == 7
    assert type(tweet[0]) == type(u'a')
    # assert type(tweet[2]) == type(6.)



def test_next(create_pickle):
    u"""This test fails on occasion, specficially when a users first tweet
    doesn't have location data."""
    users_tweets = create_pickle
    tweets = users_tweets[0]
    tweet = tweets[0]
    print tweet
    assert len(tweet) == 7
    assert type(tweet[0]) == type(u'a')

if __name__ == '__main__':
    test_query_twitter_for_histories()