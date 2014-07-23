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




    # for city, users in our_outs.items():
    #     print city, len(users)

    # for city, tweets in our_outs.items:
    #     print "\n\n", "*" * 10, "\n\n"
    #     print city, "\n\n"
    #     print len(tweets)
    #     print "\n\n", "*" * 20, "\n\n"
    # nulls = 0
    # null_keys = []
    # for key, vals in data.items():
    #     if len(vals) < 1:
    #         nulls += 1
    #         null_keys.append(key)
    # print "No values for ", nulls, " cities: ", null_keys