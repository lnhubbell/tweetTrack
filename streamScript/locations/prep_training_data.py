import tweepy
import os
from streamScript.send_data import execute_query, _get_connection
from twitter_keys import my_keys

u"""Reads in a file of cities and their bounding boxes. Queries the database
to get a list of all unique users who have tweeted from that city. Queries Twitter api
to get 200 tweets from each user, then inserts 200 tweets for up to 100 users per city
into a separate database table called "Tweet200."""


def get_twitter_api():
    #key_sets = [AltTwitterKeys, TwitterKeys, OtherAltTwitterKeys, NathansTwitterKeys]

    for our_set, our_keys in my_keys.items():
        auth = tweepy.OAuthHandler(
            our_keys['consumer_key'],
            our_keys['consumer_secret']
        )
        auth.set_access_token(
            our_keys['access_key'],
            our_keys['access_secret']
        )
        yield tweepy.API(auth)


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


def query_db(city, values):
    u"""Calls the file reading function to get in a dict of bounding boxes
    for the 100 most populous US cities. Returns a dict containing all tweets
    collected from each city (with the key being the city name and the value
    being a list of tweets)."""
    lats = values[0]
    longs = values[1]
    vals = (lats[0], lats[1], longs[0], longs[1])
    sql = """SELECT * FROM "Tweet" WHERE
        (location_lat BETWEEN %s AND %s)
        AND (location_lng BETWEEN %s AND %s); """
    print "Querying database for ", city
    data = execute_query(sql, vals, need_results=True)
    return data


def get_unique_handles(vals):
    u"""Takes in a dict with locations as the keys and a list of tweets
    as the values. Returns a dict of unique user handles for each location."""
    users = {}
    for tweet in vals:
        name = tweet[1]
        if name in users:
            users[name] += 1
        else:
            users[name] = 1
    heavy_users = []
    for user in users:
        if users[user] > 5:
            heavy_users.append(user)
    return heavy_users


def query_twitter_for_histories(users, city):
    u"""Calls function to return a dict of cities and the unique users for each
    city. Iterates over the dict to extract the tweet text/locations/timestamps
    for each tweet, bundles results into DB-friendly tuples."""
    api = get_twitter_api().next()
    city_tweets = []
    user_count = 0
    too_low_count = 0
    for user in users:
        if user_count > 100:
            break
        tweet_his = []
        history = []
        try:
            history = api.user_timeline(screen_name=user, count=200)
        except tweepy.error.TweepError as err:
            print "Tweepy Error"
            print err.message
            if err.message == "[{u'message': u'Rate limit exceeded', u'code': 88}]":
                api = get_twitter_api().next()
            continue
        if len(history) >= 200:
            user_count += 1
            for tweet in history:
                screen_name = user
                text = tweet.text
                created_at = tweet.created_at.strftime('%m/%d/%Y')
                location = tweet.geo
                if location:
                    location_lat = location['coordinates'][0]
                    location_lng = location['coordinates'][1]
                hashtags = []
                if location:
                    blob = (
                        screen_name, text, location_lat, location_lng,
                        created_at, hashtags, city
                    )
                    tweet_his.append(blob)
        if len(tweet_his):
            city_tweets.append(tweet_his)
            print user_count
        else:
            print 'not enough tweets in this users history'
            too_low_count += 1
        total = user_count + too_low_count
        print "total requests: ", total
    return city_tweets


def send_user_queries_to_db(tweet_set, city):
    u"""Sends formatted tweets into DB."""
    for blob in tweet_set:
        if blob:
            for tweet in blob:
                if tweet:
                    sql = """INSERT INTO "Tweet200" (screen_name,
                        text, location_lat, location_lng, created_at,
                        hashtags, city) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ; """
                    execute_query(sql, tweet)
                    print "Sending to database..."
    _get_connection().commit()
    with open('stop_cities.txt', 'a') as fff:
        fff.write(city)
        fff.write("\n")
    print "writing city to stop_cities file"
    print "committed tweets from ", city, " to DB"


def process_each_city():
    bb_dict = read_in_bb_file()
    for city, values in bb_dict.items():
        with open("stop_cities.txt", "r") as ffff:
            stop_cities = ffff.read()
        if city not in stop_cities:
            vals = query_db(city, values)
            print "Now checking ", city
            handles = get_unique_handles(vals)
            print city, len(handles)
            if len(handles) >= 150:
                print "Now querying twitter for histories"
                tweets = query_twitter_for_histories(handles, city)
                if len(tweets) >= 100:
                    send_user_queries_to_db(tweets, city)
                else:
                    print "Not enough users with twitter histories in ", city


if __name__ == "__main__":
    process_each_city()
