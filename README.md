# College Soccer Schools

I used https://wikitable2csv.ggor.de/ to download the tables for the following Wikipedia Pages:

- https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_men%27s_soccer_programs
- https://en.wikipedia.org/wiki/List_of_NCAA_Division_II_men%27s_soccer_programs
- https://en.wikipedia.org/wiki/List_of_NCAA_Division_III_institutions

I also downloaded the most recent [College School Card Data](https://collegescorecard.ed.gov/data/) from 

- https://ed-public-download.app.cloud.gov/downloads/Most-Recent-Cohorts-Institution_09012022.zip

Then I ran the `convert` program which uses [xsv] to combine the Wikipedia CSV datasets.
