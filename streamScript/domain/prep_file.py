u"""Uses a Census bureau list of US cities by population to return a formatted
list of the 100 most populous US cities. Uses a csv file of states and their abbreviations
to return the 2-letter mailing abbr for each state."""


with open('US_census_cities_by_pop.csv', "r") as nfile:
    lines = nfile.readlines()[1:]

state_abbrs = {}
with open("states.csv", "r") as sfile:
    s_lines = sfile.readlines()

s_lines = str(s_lines).split("\\r")

for s_line in s_lines:
    div = s_line.split(",")
    state_abbrs[div[0].lower().strip()] = div[1]

with open('locs.txt', 'w') as f:
    for line in lines[:100]:
        line = line.strip().split(",")
        out = line[8:10]
        out[0] = out[0][1:]
        new_city_name = []
        for chunk in out[0].split():
            if chunk.lower() == "st.":
                chunk = "saint"
            if chunk.lower() != "urban":
                new_city_name.append(chunk)
        out[0] = " ".join(new_city_name)
        out[1] = state_abbrs[out[1][:-1].lower().strip()]
        out = "\t".join(out)
        f.write(out + "\n")
nfile.close()
f.close()
