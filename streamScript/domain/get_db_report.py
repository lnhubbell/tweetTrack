import datetime
from get_tweets_by_user import get_unique_handles, query_db

u"""Generates a report on database stats"""


def get_data_set():
    return query_db()



def write_report():
    header = "Report generated: " + \
        datetime.datetime.now().strftime('%m/%d/%Y') + "\n\n"
    columns = 
    with open("text/db_report.txt", "w") as f:
        f.write(header)
    pass


if __name__ == "__main__":
    write_report()