from get_tweets_by_user import query_twitter_for_histories
from create_classifier import generate_predictions


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
            right, wrong, preds, actual = generate_predictions(history)
            for pred in preds:
                user = {}
                user['name'] = pred[0]
                if actual[0]:
                    user['prediction'] = actual[0]
                else:
                    user['prediction'] = pred[2]
                user['success'] = True
            return user


def generate_predictions(userTestdata):
    u"""Takes in a list of twitter users' last 200 tweets, formatted as
    'blobs'. Returns a percent correct (if known), a list of all incorrect
    guesses (or unknown), and a list of all the city predictions."""
    mnb = picklers.load_pickle('classifier_pickle')
    vocab = picklers.load_pickle('vocab_pickle')
    X, user_array, user_cities = build_test_matrix(userTestdata, vocab)
    correct = 0
    incorrect = 0
    got_wrong = []
    all_results = []
    predictions = mnb.predict_log_proba(X)
    y = picklers.load_pickle('labels_pickle')
    print user_array
    print user_cities
    print zip(tuple(y), tuple(predictions))
    if len(predictions):
        for idx, prediction in enumerate(predictions):
            report = (user_array[idx], user_cities[idx], prediction)
            if user_cities[idx] == prediction:
                correct += 1
            else:
                incorrect += 1
                got_wrong.append(report)
            all_results.append(report)
        percent_right = correct / (float(correct) + incorrect)
        return percent_right, got_wrong, all_results, user_cities


def serve_predictions(names):
    results = make_prediction(names)
    for result in results:
        yield result

if __name__ == "__main__":
    user_names = 'TrustyJohn'
    results = make_prediction(user_names)
    print "For the user: ", results['name'], " our predictions are: ", results['prediction']
