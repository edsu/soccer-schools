#!/usr/bin/env python3

import re
import pandas

def main():
    df = get_divisions()
    df = augment_doe(df)
    df.to_csv('schools.csv', index=False)

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

    return df

def augment_doe(df):
    doe = pandas.read_csv('data/Most-Recent-Cohorts-Institution.zip', low_memory=False)
    doe = doe[['INSTNM', 'ADM_RATE_ALL', 'SAT_AVG_ALL', 'COSTT4_A', 'LONGITUDE', 'LATITUDE']]
    doe.columns = ['School', 'AdmissionRate', 'SAT', 'Cost', 'Longitude', 'Latitude']

    doe['SchoolKey'] = doe['School'].map(name_key)
    df['SchoolKey'] = df['School'].map(name_key)
    df = df.merge(doe, on='SchoolKey', how='left', suffixes=['', '_y'])
    df = df.drop(['SchoolKey', 'School_y'], axis=1)

    return df

def name_key(s):
    s = s.upper()
    s = re.sub(r'\[.+?\]', '', s)
    s = re.sub(r'[^A-Z]', '', s)
    s = ''.join(sorted(s))
    return s

if __name__ == "__main__":
    main()
