import datetime
from get_tweets_by_user import get_unique_handles
from send_data import query_db, read_in_bb_file

u"""Generates a report on database stats"""


def write_report():
    bb_dict = read_in_bb_file()
    header = "Report generated: " + \
        datetime.datetime.now().strftime('%m/%d/%Y') + "\n\n"
    columns = "City,Users,Tweets\n"
    with open("text/db_report.txt", "w") as f:
        f.write(header)
        f.write(columns)
        total_tweets = 0
        total_users = 0
        out_list = []
        for city, values in bb_dict.items():
            tweets = query_db(city, values)
            handles = len(get_unique_handles(tweets))
            city_tweets = len(tweets)
            total_tweets += city_tweets
            total_users += handles
            out = ",".join([str(city), str(handles), str(city_tweets)])
            out_list.append(out)
        out_list.sort(key=lambda x: x[1])
        joined = "\n".join(out_list)
        f.write(joined)
        totals = ",".join(["Totals", str(total_users), str(total_tweets)])
        f.write(totals)

if __name__ == "__main__":
    write_report()
