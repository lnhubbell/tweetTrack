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


def serve_predictions(names):
    results = make_prediction(names)
    for result in results:
        yield result

if __name__ == "__main__":
    user_names = 'crisewing'
    results = make_prediction(user_names)
    print "For the user: ", results['name'], " our predictions are: ", results['prediction']
