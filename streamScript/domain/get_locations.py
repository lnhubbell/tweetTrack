u"""These are supporting functions that are used in the 'get_target_cities.py'
file. You should not need to run them on their own. Uses a Census bureau list
of US cities by population to return a formatted list of the 100 most populous
cities. Uses a csv file of states and their abbreviations to return the
2-letter mailing abbr for each state."""


def _open_files():
    with open('text/US_census_cities_by_pop.csv', "r") as nfile:
        lines = nfile.readlines()[1:]
    state_abbrs = {}
    with open("text/states.csv", "r") as sfile:
        s_lines = sfile.readlines()
    s_lines = str(s_lines).split("\\r")
    for s_line in s_lines:
        div = s_line.split(",")
        state_abbrs[div[0].lower().strip()] = div[1]
    return state_abbrs, lines


def _make_top_cities_list(state_abbrs, lines, n=100):
    print n
    locs_of_interest = []
    for line in lines[:n]:
        line = line.strip().split(",")
        out = line[8:10]
        out[0] = out[0][1:]
        new_city_name = []
        for chunk in out[0].split():
            if chunk.lower() == "st.":
                chunk = "Saint"
            if chunk.lower() != "urban":
                new_city_name.append(chunk)
        out[0] = " ".join(new_city_name)
        out[1] = state_abbrs[out[1][:-1].lower().strip()]
        # out = ",".join(out)
        locs_of_interest.append(out)
    return locs_of_interest


def get_locs(n=100):
    state_abbrs, lines = _open_files()
    return _make_top_cities_list(state_abbrs, lines, n)
