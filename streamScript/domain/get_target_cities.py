from get_locations import get_locs
import sys

u"""Use this file to reset the number of target cities. This is a fundamental
change. You may do it through the 'if name = main' block. Bear in mind that you
will need to rebuild your database with the new cities to get an even data
spread.

Here are some details about the file:
Reads in the bounding boxes from a csv file of bounding boxes as determined by the
min/max latitudes and longitudes of all addresses located within each
city, and prints the cities with their min/max latitudes
and longitudes to the file "bounding_boxes.txt"""


def read_in_input_files(n):
    our_locs = get_locs(n)
    with open("text/h.jarvis.csv", 'r') as ff:
        bb_lines = str(ff.readlines()).split("\\r")
    return our_locs, bb_lines


def extract_biggest_city_boxes(our_locs, bb_lines):
    found_it = []
    nyc_vals = []
    nyc_names = [
        "BRONX", "STATEN ISLAND", "LITTLE NECK", "BROOKLYN", "NEW YORK"
    ]
    our_bbs = []
    for line in bb_lines:
        line = line.split(",")
        if (line[0] in nyc_names) and (line[1] == "NY"):
            nyc_vals.append(line)
        for loc in our_locs:
            if line[1] == loc[1].upper().strip():
                w_hp = "-".join(line[0].lower().split())
                if loc[0].lower().startswith(line[0].lower()) \
                        or loc[0].lower().startswith(w_hp):
                    our_bbs.append(line)
                    found_it.append(loc[0])
    for idx, city in enumerate(our_bbs):
        if city[0].strip() == "NEW YORK":
            our_bbs[idx] = fix_nyc_vals(nyc_vals)
    return found_it, our_bbs


def fix_nyc_vals(borough_vals):
    min_lat = 0
    max_lat = 0
    min_long = 0
    max_long = 0
    for spl in borough_vals:
        if (not min_lat) or (spl[2] < min_lat):
            min_lat = spl[2]
        if spl[3] > max_lat:
            max_lat = spl[3]
        if spl[4] > max_long:
            max_long = spl[4]
        if (not min_long) or (spl[5] < min_long):
            min_long = spl[5]
    nyc_total = ["NEW YORK", "NY", min_lat, max_lat, max_long, min_long]
   # print min_lat, max_long, max_lat, min_long
    return nyc_total


def report_accuracy(our_locs, found_it):
    for loc in our_locs:
        if loc[0] not in found_it:
            print loc


def write_to_file(our_bbs):
    with open("text/test_bounding_boxes.txt", "w") as fff:
        for city in our_bbs:
            fff.write(",".join(city))
            fff.write("\r\n")


def generate_new_target_cities(n=100):
    our_locs, bb_lines = read_in_input_files(n)
    found_it, our_bbs = extract_biggest_city_boxes(our_locs, bb_lines)
    report_accuracy(our_locs, found_it)
    write_to_file(our_bbs)


if __name__ == "__main__":
    n = sys.argv[1:2]
    if not n:
        n = 100
    generate_new_target_cities(n)
