def check_city_locations(location_lat, location_lng):
    bb_dict = read_in_bb_file()
    for city, values in bb_dict.items():
        if (values[0][0] < location_lat < values[0][1]) and \
                values[1][0] < location_lng < values[1][1]:
            return city, values



def format_blob(history, user):
    u"""Formats tweets pieces to be fed to sql query.
    History is a list-like set of tweets. User is the screen name
    as a string. City is the string name of the city we querried for."""
    tweet_his = []
    locations_found = {}
    city = None
    city_lats = None
    city_lngs = None
    for tweet in history:
        screen_name = user
        text = tweet.text
        created_at = tweet.created_at.strftime('%m/%d/%Y')
        location = tweet.geo
        location_lat = None
        location_lng = None
        if location:
            location_lat = location['coordinates'][0]
            location_lng = location['coordinates'][1]
            if city_lats and city_lngs:
                between =  
        if not city or between:
            place = check_city_locations(location_lat, location_lng)
            locations_found[place[0]] = locations_found.set_default(place[0], 0) + 1
            city_lats = place[1][0]
            city_lngs = place[1][1]
        if city == place[0]:
            locations_found[place[0]] = locations_found.set_default(place[0], 0) + 1
        else:

        hashtags = []
        blob = (
            screen_name, text, location_lat, location_lng,
            created_at, hashtags, city
        )
        tweet_his.append(blob)
    return tweet_his


    ########

    """From create_classifiers""""



def build_vocab(data, n=1000):
    u"""MAY BE DEPRECATED Takes in a dict with locations as the keys
    and a list of tweets
    as the values. Returns a list of tuples (word, word count) for the
    top n words."""
    vocab = {}
    stopwords = open('text/stopwords.txt').read().lower().split()
    for key, val in data.items():
        for tweet in val:
            the_text = tweet[2]
            print the_text
            the_text = the_text.lower().split()
            for word in the_text:
                if word not in stopwords:
                    vocab[word] = vocab.setdefault(word, 0) + 1
    the_list = sorted(vocab.items(), key=lambda x: -x[1])
    return the_list[:n]


# def fit_classifier(X, y):
#     u"""Takes in an X matrix and a Y array of labels.
#     Checks four possible alpha values; returns the
#     classifier with the highest cross-validated score."""
#     best = None
#     best_score = None
#     alphas = [1E-4, 1E-3, 1E-2, 1E-1, 1]
#     for alpha in alphas:
#         mnb = MNB(alpha)
#         score = np.mean(
#             cross_val_score(mnb, X, y, cv=10)
#         )
#         if not best:
#             best = mnb
#             best_score = score
#         elif score > best_score:
#             best_score = score
#     best.fit(X, y)
#     return best, best_score
