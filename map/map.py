#!/usr/bin/env python

# Turn the New England CSV into a geo-json file.

import json
import numpy
import pandas

def make_map(input_file, output_file):
    df = pandas.read_csv(input_file)

    output = []
    for i, rec in df.iterrows():
        if numpy.isnan(rec["Longitude"]):
            continue
        output.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [rec["Longitude"], rec["Latitude"]]
            },
            "properties": rec.dropna().to_dict()
        })

    json.dump(output, open(output_file, "w"), indent=2)

if __name__ == "__main__":
    make_map("../data.csv", "data.json")
