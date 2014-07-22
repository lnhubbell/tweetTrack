
def read_in_input_files():
    our_locs = []
    with open("locs.txt", 'r') as f:
        lines = f.readlines()
    f.close()

    for line in lines:
        div = line.lower().split("\t")
        our_locs.append(div)

    with open("h.jarvis.csv") as ff:
        bb_lines = str(ff.readlines()).split("\\r")
    ff.close()

    return our_locs, bb_lines


def extract_biggest_city_boxes(our_locs, bb_lines):
    found_it = []
    nyc_vals = []
    nyc_names = ["BRONX", "STATEN ISLAND", "LITTLE NECK", "BROOKLYN", "NEW YORK"]
    our_bbs = []
    for line in bb_lines:
        line = line.split(",")
        if (line[0] in nyc_names) and (line[1] == "NY"):
            nyc_vals.append(line)
        for loc in our_locs:
            if line[1] == loc[1].upper().strip():
                w_hp = "-".join(line[0].lower().split())
                if loc[0].startswith(line[0].lower()) or loc[0].startswith(w_hp):
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
    with open("bounding_boxes.txt", "w") as fff:
        for city in our_bbs:
            fff.write(",".join(city))
            fff.write("\r\n")


if __name__ == "__main__":
    our_locs, bb_lines = read_in_input_files()
    found_it, our_bbs = extract_biggest_city_boxes(our_locs, bb_lines)
    report_accuracy(our_locs, found_it)
    write_to_file(our_bbs)
