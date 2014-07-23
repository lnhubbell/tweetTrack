import numpy as np
import cPickle
import tweepy

from sklearn.feature_extraction.text import CountVectorizer as CV
from sklearn.naive_bayes import MultinomialNB as MNB
from sklearn.cross_validation import cross_val_score

from streamScript.send_data import execute_query, _get_connection
from twitter_keys import my_keys

u"""Reads in a file of cities and their bounding boxes. Queries the
database to get a list of all unique users who have tweeted from that
city. Queries Twitter api to get 200 tweets from each user, then inserts
200 tweets for up to 100 users per city
into a separate database table called "Tweet200."""


def get_twitter_api():
    u"""Gets twitter keys from key file."""
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


def query_all_db(new_pickle=False):
    i = 0
    bb_dict = read_in_bb_file()
    data_set = {}
    for key, values in bb_dict.items():
        data = query_db(key, values)
        data_set[key] = data
        i += 1
    if new_pickle:
        pickle_file = open('pickle', 'w')
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
    stopwords = open('stopwords.txt').read().lower().split()
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
    stopwords = open('stopwords.txt').read().lower().split()
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


def format_blob(history, user, city):
    u"""Formats tweets pieces to be fed to sql query."""
    tweet_his = []
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
    return tweet_his


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
        history = []
        try:
            history = api.user_timeline(screen_name=user, count=200)
        except tweepy.error.TweepError as err:
            print "Tweepy Error: ", err.message
            if err.message == "[{u'message': u'Rate limit \
                    exceeded', u'code': 88}]":
                api = get_twitter_api().next()
            continue
        if len(history) >= 200:
            user_count += 1
            tweet_his = format_blob(history, user, city)
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
    u"""Calls functions to insert user data into Tweet200 table."""
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
    try:
        pickle_file = open('pickle', 'rb')
        print "Loading Pickle..."
        data = cPickle.load(pickle_file)
        print "Pickle loaded."
        pickle_file.close()
    except IOError:
        data = query_db(True)

    top_words = build_matrix(data, 5000)
    print "Pickling..."
    pickle_file = open('xypickle', 'w')
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
