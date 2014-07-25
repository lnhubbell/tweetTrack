from get_tweets_by_user import query_twitter_for_histories
from create_classifier import build_test_matrix
import picklers


def generate_predictions(userTestdata):
    u"""Takes in a list of twitter users' last 200 tweets, formatted as
    'blobs'. Returns a percent correct (if known), a list of all incorrect
    guesses (or unknown), and a list of all the city predictions."""
    mnb = picklers.load_pickle('classifier_pickle')
    vocab = picklers.load_pickle('vocab_pickle')
    X, user_name, user_city = build_test_matrix(userTestdata, vocab)
    prediction = mnb.predict(X)
    report = (user_name, user_city, prediction[0])
    return report


def make_prediction(name):
    u"""Takes in a list of Twitter user handles. Returns a list of
    single-entry dictionaries, with the keys being the user names
    and the values being the predictions."""
    print "Name: " + str(name)
    name = [name]
    histories = query_twitter_for_histories(name, data_collection=False)
    for history in histories:
        if len(history) < 100:
            user = {}
            user['name'] = history[0][0]
            user['prediction'] = """You're not cool enough to track!"""
            user['success'] = False
            return user
            print "Not Long enough"
        else:
            print "Long enough"
            user_name, user_city, prediction = generate_predictions(history)
            user = {}
            user['name'] = user_name
            if user_city:
                user['prediction'] = city
            else:
                user['prediction'] = prediction
            user['success'] = True
            return user


def predict_on_list(user_names):
    u"""Takes in a list of tuples, where the first element is the user name,
    and the second element is the known city location. Prints to the terminal
    a report of the number correct, a list of the wrong guesses, and a list
    of the correct guesses. Returns the percent correct."""
    correct = 0
    incorrect = 0
    got_wrong = []
    got_right = []
    for name, actual_city in user_names:
        results = make_prediction(name)
        if results['success']:
            incorrect += 1
            got_wrong.append(results)
        elif results['prediction'] == 



        print "For the user: ", results['name'], " our predictions are: ", results['prediction']


if __name__ == "__main__":
   pass

