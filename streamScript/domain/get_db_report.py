import datetime
from get_tweets_by_user import get_unique_handles
from send_data import query_all_db, query_all_db_Tweet200

u"""Generates a csv report on database stats. Currently set to
query the Tweet200 database."""


def write_report():
    print "Querying Tweet 200 table"
    header = "Report generated: " + \
        datetime.datetime.now().strftime('%m/%d/%Y') + ", " +\
        datetime.datetime.now().strftime('%H:%M') + "\n\n"
    columns = "City,Users,Tweets\n"
    with open("text/db_Tweet200_report.txt", "w") as f:
        f.write(header)
        f.write(columns)
        total_tweets = 0
        total_users = 0
        out_list = []
        for city, tweets in query_all_db_Tweet200().items():
            handles = len(get_unique_handles(tweets))
            city_tweets = len(tweets)
            total_tweets += city_tweets
            total_users += handles
            out = ",".join([str(city), str(handles), str(city_tweets)])
            out_list.append(out)
        out_list.sort(key=lambda x: x[-1])
        joined = "\n".join(out_list)
        f.write(joined)
        f.write("\n")
        totals = ",".join(["Totals", str(total_users), str(total_tweets)])
        star_line = ("*" * 10) + "\n"
        f.write(star_line)
        f.write(totals)
        f.write("\n")
        f.write(star_line)

if __name__ == "__main__":
    write_report()
