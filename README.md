# College Soccer Schools

My son is interested in playing soccer at College and I wanted to get a dataset
of colleges and universities with their associated conference and division,
average SAT score, acceptance rate and annual cost. Maybe there's a way to do
this using existing tools but what better way to sublimate the stress by doing
this myself? 

I started by using https://wikitable2csv.ggor.de/ to download the tables for
the following Wikipedia Pages:

- https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_men%27s_soccer_programs
- https://en.wikipedia.org/wiki/List_of_NCAA_Division_II_men%27s_soccer_programs
- https://en.wikipedia.org/wiki/List_of_NCAA_Division_III_institutions

Then I downloaded the most recent [College School Card Data](https://collegescorecard.ed.gov/data/) from 

- https://ed-public-download.app.cloud.gov/downloads/Most-Recent-Cohorts-Institution_09012022.zip

The `convert.py` program will:

1. Merge and normalize the division CSVs
2. Reconcile the school names against Wikidata
3. Get additional information from Wikidata (postal code, student count, admission rate, location)
4. Join the data College School Card data using the postal code to get the admission rate, cost-per-year, average SAT, and admission rate.
5. The `missing-wikidata.csv` contains rows for schools that weren't reconciled against Wikidata
6. The `missing-postalcode.csv` files contains rows for Wikidata entities that lacked a postal code
7. Writes out the resulting data to `data.csv`

