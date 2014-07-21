from send_data import execute_query
from tweetTrack.app.config.keys import TwitterKeys
from tweetTrack.app.views import get_twitter_api
from .streamScript.twitter_stream import StdOutListener
import json


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


def query_db():
    u"""Calls the file reading function to get in a dict of bounding boxes
    for the 100 most populous US cities. Returns a dict containing all tweets
    collected from each city (with the key being the city name and the value
    being a list of tweets)."""
    bb_dict = read_in_bb_file()
    data_set = {}
    for key, values in bb_dict.items():
        lats = values[0]
        longs = values[1]
        vals = (lats[0], lats[1], longs[0], longs[1])
        sql = """SELECT * FROM "Tweet" WHERE (location_lat BETWEEN %s AND %s) AND (location_lng BETWEEN %s AND %s); """
        print "Querying database..."
        data = execute_query(sql, vals)
        data_set[key] = data

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
    #l = StdOutListener()
    whole_set = {}
    for city, users in users_by_city.items():
        city_tweets = []
        user_count = 0
        while user_count < 1:
            for user in users:
                tweet_his = []
                history = api.user_timeline(screen_name=user, count=200)
                if len(history) >= 200:
                    user_count += 1
                    for tweet in history:
                        #blob = get_data(tweet)
                        #tweet_his.append(blob)
                        tweet_his.append(tweet)
                    city_tweets.append(tweet_his)
        whole_set[city] = city_tweets
    return whole_set


if __name__ == "__main__":
    data = query_db()
    our_outs = query_twitter_for_histories(data)

    for city, tweets in our_outs.items:
        print "\n\n", "*" * 10, "\n\n"
        print city, "\n\n"
        print tweets
        print "\n\n", "*" * 20, "\n\n"
    # nulls = 0
    # null_keys = []
    # for key, vals in data.items():
    #     if len(vals) < 1:
    #         nulls += 1
    #         null_keys.append(key)
    # print "No values for ", nulls, " cities: ", null_keys


