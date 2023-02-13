# College Soccer Schools

My son is interested in playing soccer at college and I wanted to get a dataset
of colleges and universities with their associated conference and division,
average SAT score, acceptance rate and annual cost. Maybe there's a way to do
this using existing tools but what better way to sublimate/repress the stress
by turning this into a data problem. 

I started by using [wikitable2csv] to download the tables for the following Wikipedia Pages:

- https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_men%27s_soccer_programs
- https://en.wikipedia.org/wiki/List_of_NCAA_Division_II_men%27s_soccer_programs
- https://en.wikipedia.org/wiki/List_of_NCAA_Division_III_institutions

Then I downloaded the most recent [College School Card Data] from:

- https://ed-public-download.app.cloud.gov/downloads/Most-Recent-Cohorts-Institution_09012022.zip

All these files are in the `data` directory. Then I ran the `convert.py` program to:

1. Merge and normalize the division CSVs.
2. Join the data College School Card data, to add the admission rate, cost-per-year, average SAT, and geo-location.
3. Write out the resulting data to `schools.csv`.

You can see that there is quite a bit of schools (10%) that didn't get joined due to very different school names. The natural key I used was to capitalize the name, remove all punctuation and then sort the letters. Other approaches would be welcome!

The `new-england.csv` subset was created by extracting New England schools (plus New York) for a trip we were planning to visit a few schools.

[wikitable2csv]: https://wikitable2csv.ggor.de/ 
[College School Card Data]: https://collegescorecard.ed.gov/data/


