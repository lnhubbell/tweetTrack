import tweepy
from streamScript.twitter_stream import get_data
from streamScript.send_data import execute_query
from sklearn.feature_extraction.text import CountVectorizer as CV
from sklearn.naive_bayes import MultinomialNB as MNB
from sklearn.cross_validation import cross_val_score
import numpy as np
import cPickle

u"""Reads in a file of cities and their bounding boxes. Queries the database
to get a list of all unique users who have tweeted from that city. Queries Twitter api
to get 200 tweets from each user, then inserts 200 tweets for up to 100 users per city
into a separate database table called "Tweet200."""


class TwitterKeys(object):
    consumer_key = 'hWMHWIJYoJ4UIG0KNwXcC4pbg'
    consumer_secret = '85E7dAk4ZkJEyNkQ0EbxYvavL7FeKUwEEJlXOs9QnXDwIcWL5c'
    access_key = '249913463-xJhkkoiipEVF0xIJeZc9dys8N1qovmZGmgqiSLaV'
    access_secret = 'q4CleTUfctg4BfQz6R5cRpa8EekBylIRzr63fCuargyDa'


def get_twitter_api():
    auth = tweepy.OAuthHandler(
        TwitterKeys.consumer_key,
        TwitterKeys.consumer_secret
    )
    auth.set_access_token(
        TwitterKeys.access_key,
        TwitterKeys.access_secret
    )
    return tweepy.API(auth)


def read_in_bb_file():
    u"""Reads in a file containing the 100 most populous cities in the US
    and returns a dict with the lat/long points describig the bounding box
    for each location."""
    with open("bounding_boxes.txt", 'r') as f:
        bbs = f.readlines()
    f.close()

    bb_dict = {}
    for line in bbs:
        spl = line.strip().split(",")
        city = spl[0].title()
        place_name = city + ", " + spl[1]
        lats_longs = [(spl[2], spl[3]), (spl[4], spl[5])]
        bb_dict[place_name] = lats_longs
    return bb_dict


def query_db(new_pickle=False):
    u"""Calls the file reading function to get in a dict of bounding boxes
    for the 100 most populous US cities. Returns a dict containing all tweets
    collected from each city (with the key being the city name and the value
    being a list of tweets)."""
    i = 0
    bb_dict = read_in_bb_file()
    data_set = {}
    for key, values in bb_dict.items():
        lats = values[0]
        longs = values[1]
        vals = (lats[0], lats[1], longs[0], longs[1])
        sql = """SELECT * FROM "Tweet" WHERE (location_lat BETWEEN %s AND %s) AND (location_lng BETWEEN %s AND %s) LIMIT 10000; """
        print "Querying database..." + str(i)
        data = execute_query(sql, vals)
        data_set[key] = data
        i += 1
    if new_pickle:
        pickle_file = open('pickle','w')
        cPickle.dump(data_set, pickle_file)
        pickle_file.close()
        print "Created Pickle"
    return data_set


def get_unique_handles(data):
    u"""Takes in a dict with locations as the keys and a list of tweets
    as the values. Returns a dict of unique user handles for each location."""
    users_by_city = {}
    for key, vals in data.items():
        users = {}
        for tweet in vals:
            name = tweet[1]
            if name in users:
                users[name] += 1
            else:
                users[name] = 1
        users_by_city[key] = users
    return users_by_city


def query_twitter_for_histories(data):
    users_by_city = get_unique_handles(data)
    api = get_twitter_api()
    whole_set = {}
    for city, users in users_by_city.items():
        city_tweets = []
        user_count = 0
        while user_count < 1:
            for user in users:
                tweet_his = []
                history = []
                try:
                    history = api.user_timeline(screen_name=user, count=20)
                except tweepy.error.TweepError as err:
                    print "got a tweepy error"
                    print err.message
                if len(history) >= 20:
                    user_count += 1
                    for tweet in history:
                        screen_name = user
                        text = tweet.text
                        created_at = tweet.created_at
                        location = tweet.geo
                        if location:
                            location_lat = location['coordinates'][0]
                            location_lng = location['coordinates'][1]
                        hashtags = []
                        # try:
                        #     hashtags = [i['text'] for i in tweet.entities.hashtags]
                        # except AttributeError:
                        #     print "attribute error"
                        if location:
                            blob = (
                                screen_name, text, location_lat, location_lng,
                                created_at, hashtags, city
                            )
                            tweet_his.append(blob)
                    if len(tweet_his):
                        city_tweets.append(tweet_his)
                        print "added one!"
                        print city_tweets
        whole_set[city] = city_tweets
    return whole_set


def send_user_queries_to_db(tweet_set):
    for city, blobs in tweet_set:
        for blob in blobs:
            if blob:
                sql = """INSERT INTO "Tweet200" (screen_name, text, location_lat, location_lng, created_at, hashtags, city) VALUES (%s, %s, %s, %s, %s, %s, %s); """
                execute_query(sql, blob)
                print "Sending to database..."


if __name__ == "__main__":
    data = query_db()
    our_outs = get_unique_handles(data)
    #our_outs = query_twitter_for_histories(data)
    #send_user_queries_to_db(our_outs)

    for city, users in our_outs.items():
        print city, len(users)

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


