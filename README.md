# College Soccer Schools

<a href="https://edsu.github.io/soccer-schools/map/"><img style="max-width: 800" src="https://github.com/edsu/soccer-schools/blob/main/images/map.png?raw=true"></a>

My son is interested in playing soccer at college and I wanted to get a dataset
of colleges and universities with their associated conference and division,
average SAT score, acceptance rate and annual cost. Maybe there's a way to do
this using existing tools but what better way to deal with the stress by
turning this into a data problem! 

I started by using [wikitable2csv] to download the tables for the following Wikipedia Pages:

- https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_men%27s_soccer_programs
- https://en.wikipedia.org/wiki/List_of_NCAA_Division_II_men%27s_soccer_programs
- https://en.wikipedia.org/wiki/List_of_NCAA_Division_III_institutions

Then I downloaded the most recent [College School Card Data] from:

- https://ed-public-download.app.cloud.gov/downloads/Most-Recent-Cohorts-Institution_09012022.zip

All these files are in the `data` directory. Then I ran the `convert.py` program to:

1. Merge and normalize the division tables into a CSV (data/divisions.csv).
2. Join the schools with the College Score Card data to get the SAT, Cost and geo-coordinates.
3. Write out the matches (data.csv) and schools that didn't match (missing.csv) as well as a map where the D1 schools are black, D2 are blue and D3 are red.


I originally tried using the Wikidata reconciliation service on both datasets and then joining based on WikidataID. But I ran into issues where there were false positives, perhaps because I wasn't also using the city and state as part of the reconciliation.

A simple school name match wasn't good enough (562/854 matches). After some experimentation I ended up using the state to limit the matches for each school, and then using a [Levenshtein Distance](https://en.wikipedia.org/wiki/Levenshtein_distance) to find the best match (785/854 matches). When I get around to it I'll manually match up the remaining 70.

[wikitable2csv]: https://wikitable2csv.ggor.de/ 
[College School Card Data]: https://collegescorecard.ed.gov/data/
