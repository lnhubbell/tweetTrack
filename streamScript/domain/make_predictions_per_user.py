from get_tweets_by_user import query_twitter_for_histories
from create_classifier import build_test_matrix
from query_db import query_for_handles
import picklers
import random


def generate_predictions(userTestdata, testing):
    u"""Takes in a list of twitter users' last 200 tweets, formatted as
    'blobs'. Returns a percent correct (if known), a list of all incorrect
    guesses (or unknown), and a list of all the city predictions."""
    mnb = picklers.load_pickle('classifier_pickle')
    vocab = picklers.load_pickle('vocab_pickle')
    X, user_name, user_city = build_test_matrix(userTestdata, vocab, testing)
    prediction = mnb.predict(X)
    report = (user_name, user_city, prediction[0])
    return report


def make_prediction(name, testing=False):
    u"""Takes in a list of Twitter user handles. Returns a list of
    single-entry dictionaries, with the keys being the user names
    and the values being the predictions."""
    print "Name: " + name
    name = [name]
    try:
        history = query_twitter_for_histories(name, data_collection=False)[0]
        if len(history) < 50:
            can_predict = False
            print "length was too small"
        else:
            print "length was good"
            can_predict = True
    except Exception:
        print "Twitter query failed."
        can_predict = False
    if can_predict:
        user_name, user_city, prediction = \
            generate_predictions(history, testing)
        user = {}
        user['name'] = user_name
        if user_city:
            user['prediction'] = user_city.upper()
        else:
            user['prediction'] = prediction.upper()
        user['success'] = True
    else:
        user = {}
        user['name'] = name
        user['prediction'] = """You're not cool enough to track!"""
        user['success'] = False
        print "Could not make a prediction."
    return user


def create_test_user_set():
    user_names = query_for_handles()
    picklers.write_pickle(user_names, 'known_users_pickle')


def predict_on_list(user_names):
    u"""Takes in a list of tuples, where the first element is the user name,
    and the second element is the known city location. Prints to the terminal
    a report of the number correct, a list of the wrong guesses, and a list
    of the correct guesses. Returns the percent correct."""
    correct = 0
    incorrect = 0
    got_wrong = []
    got_right = []
    count = 0
    for name, actual_city in user_names:
        count += 1
        results = make_prediction(name[0], testing=True)
        print count, "of ", len(user_names)
        if (results['success']) and \
                (results['prediction'] == actual_city.upper()):
            correct += 1
            got_right.append(results)
        else:
            incorrect += 1
            results['actual'] = actual_city.upper()
            got_wrong.append(results)
    accuracy = correct / (float(correct) + incorrect)
    print "Our accuracy on this set is: ", accuracy
    print "*" * 10
    print "We made incorrect predictions for these ", incorrect, " users: "
    for user in got_wrong:
        print "For the user: ", user['name'], \
            " our prediction was: ", user['prediction']
        print "The actual city was: ", user['actual']
    print "*" * 10
    print "We made correct predictions for these ", correct, " users: "
    for user in got_right:
        print "For the user: ", user['name'], \
            " our prediction was: ", user['prediction']
    print "*" * 10
    return accuracy

if __name__ == "__main__":
    user_names = query_for_handles()
    picklers.write_pickle(user_names, 'known_users_pickle')
    #user_names = picklers.load_pickle('known_users_pickle')
    print len(user_names)
    test_users = []
    for i in range(100):
        test_users.append(random.choice(user_names))
    # #test_users = [('TrustyJohn', 'SEATTLE, WA')]
    print predict_on_list(test_users)
