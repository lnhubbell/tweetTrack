"""This file is intended to be used as a playground to analyze data pulled
from the database. The code below was used to analyze data from the Tweet200
database, but this is a good place for any sort of extra analysis."""

def count_unique_users(data, n=10000):
    u""" Uses blocks of tweets from single users per city.
    Takes in a raw dataset and an optional parameter to limit the feature
    set to n. Defaults to 10000. Returns a tuple containing a matrix of n features,
    a vector of labels, and a vocabulary list of the features examined."""
    user_matrix = []
    user_array = []
    for key, val in data.items():
        user_list = []
        count = 0
        user_count = 0
        # print key
        print len(val)
        for ind, tweet in enumerate(val):
            # print user_count
            if user_count >= 110:
                # print "MORE THAN A THOUSAND!!!"
                continue
            if count == 0:
                this_user = tweet[1]
                our_string = ""
            if (tweet[1] == this_user) and (count < 200):
                our_string += tweet[2].lower()
                count += 1
            elif (tweet[1] != this_user): # and len(our_string) >= 14000:
                count = 0
                user_count += 1
                print ind, tweet[1],this_user
                user_matrix.append(our_string)
                user_array.append(key)
                user_list.append(this_user)
            # elif tweet[1] != this_user:
            #     count = 0
        # print len(user_matrix)
        # print len(user_array)
        # print "----------Break---------"
        # last_user = None
        # unique_users = []
        # for user in user_list:
        #     if user != last_user:
        #         unique_users.append(user)
        #     last_user = user
        # print len(unique_users)

        # user_list = []
    return user_matrix, user_array, n