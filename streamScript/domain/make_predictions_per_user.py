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
    right, wrong, preds, actual = generate_predictions(get_preds)
    for idx, pred in enumerate(preds):
        user = {}
        user['name'] = pred[0]
        if actual[idx]:
            user['prediction'] = actual[idx]
        else:
            user['prediction'] = pred[2]
        results.append(user)
    return results


def serve_predictions(names):
    results = make_prediction(names)
    for result in results:
        yield result

if __name__ == "__main__":
    user_names = ['crisewing', 'TrustyJohn']
    results = make_prediction(user_names)
    for result in results:
        print "For the user: ", result['name'], " our predictions are: ", result['prediction']
