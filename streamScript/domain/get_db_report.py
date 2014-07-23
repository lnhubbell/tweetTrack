from create_classifier import query_all_db
from get_tweets_by_user import get_unique_handles

u"""Generates a report on database stats"""


def get_data_set():
    return query_all_db()



def write_report():
    pass


if __name__ == "__main__":
    write_report()