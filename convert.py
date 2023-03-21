#!/usr/bin/env python3

import pandas
import logging
import textdistance

logging.basicConfig(filename='convert.log', level=logging.DEBUG)

def main():
    div = get_divisions()
    div.to_csv('data/divisions.csv', index=False)

    doe = get_doe()
    doe.to_csv('data/doe.csv', index=False)

    colleges, missing = join(div, doe)
    colleges.to_csv('data.csv', index=False)
    missing.to_csv('missing.csv', index=False)

def get_divisions():
    # Division 1
    d1 = pandas.read_csv('data/List_of_NCAA_Division_I_men%27s_soccer_programs_1.csv')
    d1 = d1[['Institution','Location','State', 'Conference']]
    d1.columns = ['School', 'City', 'State', 'Conference']
    d1['Division'] = 'D1'

    # Division 2
    d2 = pandas.read_csv('data/List_of_NCAA_Division_II_men%27s_soccer_programs_1.csv')
    d2 = d2[['School', 'City', 'State/Province', 'Conference']]
    d2.columns = ['School', 'City', 'State', 'Conference']
    d2['Division'] = 'D2'

    # Division 3
    d3 = pandas.read_csv('data/List_of_NCAA_Division_III_institutions_1.csv')
    d3 = d3[['School', 'City', 'State', 'Conference']]
    d3['Division'] = 'D3'

    # Join the divisions into one dataset
    df = pandas.concat([d1, d2, d3], ignore_index=True)

    # Remove newlines and abbreviations from the school name
    df['School'] = df['School'].str.replace(r' *\n *', ' ', regex=True)
    df['School'] = df['School'].str.replace(r' *\(.+\) *', '', regex=True)
    df['State'] = df['State'].str.replace('D.C.', 'District of Columbia')

    states = pandas.read_csv('data/states.csv')
    df = df.merge(states, how='left', on='State')

    return df

def get_doe():
    doe = pandas.read_csv('data/Most-Recent-Cohorts-Institution.zip', low_memory=False)
    doe = doe[['INSTNM', 'CITY', 'STABBR', 'OPEID', 'ADM_RATE_ALL', 'SAT_AVG_ALL', 'COSTT4_A', 'LONGITUDE', 'LATITUDE']]
    doe.columns = ['School', 'City', 'StateCode', 'OPEID', 'AdmissionRate', 'SAT', 'Cost', 'Longitude', 'Latitude']

    return doe

def join(div, doe):
    matches = []
    missing = []
    for _, d in div.iterrows():
        match = find_college(d, doe)
        if match is not None:
            rec = d.to_dict()
            rec.update(match.to_dict())
            matches.append(rec)
        else:
            missing.append(d)
    matches = pandas.DataFrame(matches)
    missing = pandas.DataFrame(missing)
    return matches, missing
        
def find_college(div, doe):
    school = div.School.upper()
    doe = doe[(doe.City.str.upper() == div.City.upper()) & (doe.StateCode == div.StateCode)].copy()
    doe['Lev'] = doe.School.apply(lambda s: textdistance.levenshtein(s.upper(), school))
    doe = doe.sort_values('Lev', ascending=True)

    if len(doe) == 0:
        logging.warning("No match for %s %s, %s", div.School, div.City, div.StateCode)
        return None

    match = doe.iloc[0]
    if match['Lev'] > len(school) * .1:
        logging.warning("String match lower than threshold for %s and %s", div.School, match.School)
        return None
    else:
        logging.debug('Matched "%s" to "%s" lev=%i', div.School, match.School, match.Lev)
    return match

if __name__ == "__main__":
    main()
