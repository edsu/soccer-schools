#!/usr/bin/env python

# Turn the New England CSV into a geo-json file.

import json
import numpy
import pandas

df = pandas.read_csv("data.csv")

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

json.dump(output, open("data.json", "w"), indent=2)
