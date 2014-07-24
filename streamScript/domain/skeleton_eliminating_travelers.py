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