from get_tweets_by_user import query_twitter_for_histories


def return_results():
    pass


def make_prediction(names):
    if isinstance(names, basestring):
        names = [names]
    histories = query_twitter_for_histories(names)
    for history in histories:
        if len(history) < 100:
            return history[:1][0], "Not enough tweets in this user's history."
        else:




