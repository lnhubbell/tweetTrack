from get_tweets_by_user import query_twitter_for_histories
from create_classifier import generate_predictions


def make_prediction(names):
    u"""Takes in a list of Twitter user handles. Returns a list of
    single-entry dictionaries, with the keys being the user names
    and the values being the predictions."""
    if isinstance(names, basestring):
        names = [names]
    histories = query_twitter_for_histories(names)
    results = []
    get_preds = []
    for history in histories:
        if len(history) < 100:
            user = {}
            user['name'] = history[0][0]
            user['prediction'] = """Not enough tweeting history to
                                make a prediction."""
            results.append(user)
        else:
            get_preds.append(history)
    percent_right, got_wrong, all_results = generate_predictions(get_preds)
    for prediction in all_results:
        user = {}
        user['name'] = prediction[0]
        user['prediction'] = prediction[2]
        results.append(user)
    return results


def serve_predictions(names):
    results = make_prediction(names)
    for result in results:
        yield result

if __name__ == "__main__":
    print
    # user_names = raw_input("Please enter a list of Twitter handles.\n ")
    # if not isinstance(user_names, list):
    #     user_names = raw_input("Names must be in a list.")
    #'EdgarandtheHall'
    user_names = [
        'selfiequeenbri', 'bobiiniicole', 'THE 1Far Above', 'duqe', 'neo rama']
    results = make_prediction(user_names)
    for result in results:
        print "For the user: ", result['name']
        print "Our predictions are: "
        print result['prediction']
