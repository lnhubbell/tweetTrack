import os
import psycopg2
import time
# from filters_json import filter_list as FilterMap

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

QUERY_STRINGS = {}
DB_CONFIG = {}

ROOT_DIR = os.path.abspath(os.getcwd())


def read_in_bb_file():
    u"""Reads in a file containing the 100 most populous cities in the US
    and returns a dict with the lat/long points describing the bounding box
    for each location."""
    with open("text/bounding_boxes.txt", 'r') as f:
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


def query_all_db(limit=False):
    u"""Returns a dictionary with keys as city names and values as a list of
    tweets from that city."""
    bb_dict = read_in_bb_file()
    data_set = {}
    for key, values in bb_dict.items():
        data = query_db(key, values, limit)
        data_set[key] = data
    return data_set


def query_db(city, values, limit=False):
    u"""Takes in a city and Returns a dict containing all tweets
    collected from the city (with the key being the city name and the value
    being a list of tweets)."""
    lats = values[0]
    longs = values[1]
    vals = (lats[0], lats[1], longs[0], longs[1])
    if limit:
        sql = """SELECT * FROM "Tweet" WHERE
            (location_lat BETWEEN %s AND %s)
            AND (location_lng BETWEEN %s AND %s)LIMIT 3000;"""
    else:
        sql = """SELECT * FROM "Tweet" WHERE
            (location_lat BETWEEN %s AND %s)
            AND (location_lng BETWEEN %s AND %s);"""
            ## LIMIT 2000
    print "Querying database for ", city
    data = execute_query(sql, vals, need_results=True)
    return data


def query_all_db_Tweet200():
    u"""Returns a dictionary with keys as city names and values as a list of
    tweets from that city."""
    bb_dict = read_in_bb_file()
    data_set = {}
    for key, values in bb_dict.items():
        sql = """SELECT * FROM "Tweet200" WHERE city == %s;"""
        data = execute_query(sql, key, need_results=True)
        data_set[key] = data
    return data_set


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
                    execute_query(sql, tweet, autocommit=False)
                    print "Sending to database..."
    DB_CONFIG['DB_CONNECTION'].commit()
    print "we committed"
    with open('text/stop_cities.txt', 'a') as fff:
        fff.write(city)
        fff.write("\n")
    print "writing city to stop_cities file"
    print "committed tweets from ", city, " to DB"


def execute_query(sql, args=None, need_results=False, autocommit=True):
    u"""execute the passed in SQL using the current cursor.
    If the query string takes any args pass those to the cursor as well."""
    _get_connection_string()
    results = None
    try:
        cur = _get_cursor()
        cur.execute(sql, args)
        if need_results:
            results = cur.fetchall()
    except psycopg2.Error as x:
        # this will catch any errors generated by the database
        print "*" * 40
        print "Error executing query against DB: ", x.args
        print "Attempting to reconnect to the DB..."
        DB_CONFIG['DB_CONNECTION'].close()
        DB_CONFIG['DB_CONNECTION'] = None
        DB_CONFIG['DB_CURSOR'] = None
        time.sleep(5)
        conn = _get_connection()
        while conn is None:
            conn = _get_connection()
            time.sleep(5)
    else:
        if autocommit:
            DB_CONFIG['DB_CONNECTION'].commit()
    return results


def _get_cursor():
    """get the current cursor if it exist, else create a new cursor"""
    cur = DB_CONFIG.get('DB_CURSOR')
    if cur is not None:
        # print "cursor exists, using that..."
        return cur
    else:
        # print "no cursor found, so creating one..."
        return _create_cursor()


def _create_cursor():
    """create a new cursor and store it"""
    conn = _get_connection()
    # print "creating new cursor..."
    DB_CONFIG['DB_CURSOR'] = conn.cursor()
    # print "got new cursor."
    return DB_CONFIG['DB_CURSOR']


def _get_connection():
    """Get the current connection if it exists, else connect."""
    conn = DB_CONFIG.get('DB_CONNECTION')
    if conn is not None:
        # print "connection exists, so reusing it..."
        return conn
    else:
        # print "no connection found..."
        return _connect_db()


def _connect_db():
    try:
        # print "establishing a new connection..."
        conn = psycopg2.connect(DB_CONFIG['DB_CONNECTION_STRING'])
    except Exception:
        raise Exception("Error connecting to DB: " +
                        str(DB_CONFIG['DB_CONNECTION_STRING']))
    # print "Connection established and stored..."
    DB_CONFIG['DB_CONNECTION'] = conn
    return conn


def _get_connection_string():
    password = _get_pasword()
    connection_string = []
    connection_string.append(
        "host=tweetstalk.cvf1ij0yeyiq.us-west-2.rds.amazonaws.com"
    )
    connection_string.append("dbname=lil_tweetstalker")
    connection_string.append("user=tweetstalkers")
    connection_string.append("password=")
    connection_string.append(password)
    connection_string.append("port=5432")
    connection = " ".join(connection_string)

    DB_CONFIG['DB_CONNECTION_STRING'] = connection


def _get_pasword():
    password = open(ROOT_DIR + '/our_keys/config').read().split()
    return password[1]


def add_rows():
    sql = """INSERT INTO "Tweet" (screen_name, text, location_lat, location_lng, created_at, hashtags) SELECT screen_name, text, location_lat, location_lng, created_at, hashtags FROM "TweetTest";"""
    print "Querying database"
    execute_query(sql)


def change_col_size():
    sql = """ ALTER TABLE "Tweet" ALTER COLUMN text TYPE varchar(200);"""
    print "Querying database"
    execute_query(sql)

if __name__ == "__main__":
    pass
    #add_rows()
    # change_col_size()


