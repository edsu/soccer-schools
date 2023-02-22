#!/usr/bin/env python3

import pandas
import logging
import reconciler

logging.basicConfig(filename='convert.log', level=logging.DEBUG)

def main():

    print("Reconciling NCAA division schools with Wikidata...")
    div = get_divisions()
    div, div_missing = reconcile(div)
    div.to_csv('data/divisions.csv', index=False)
    div_missing.to_csv('data/missing_div.csv', index=False)

    print("Reconciling DOE College School Card data with Wikidata...")
    doe = get_doe()
    doe, doe_missing = reconcile(doe)
    doe.to_csv('data/doe.csv', index=False)
    doe_missing.to_csv('data/missing_doe.csv', index=False)
    
    colleges = merge(div, doe)
    colleges.to_csv('colleges.csv', index=False)

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

def get_doe():
    doe = pandas.read_csv('data/Most-Recent-Cohorts-Institution.zip', low_memory=False)
    doe = doe[['INSTNM', 'OPEID', 'ADM_RATE_ALL', 'SAT_AVG_ALL', 'COSTT4_A']]
    doe.columns = ['School', 'OPEID', 'AdmissionRate', 'SAT', 'Cost']

    return doe

def reconcile(df):
    # reconcile against Wikidata entities of type higher education institution
    recon = reconciler.reconcile(df['School'], type_id='Q38723')
    recon = recon[['id', 'input_value', 'score']]

    # merge the results, and drop/rename columns
    df = df.merge(recon, left_on='School', right_on='input_value', how='left')
    df = df.drop(['input_value'], axis=1)
    df = df.rename({'id': 'WikidataID', 'score': 'Score'}, axis=1)

    # track and remove rows that were missing WikidataIDs
    missing = df[df['WikidataID'].isnull()]
    df = df[~df['WikidataID'].isnull()]

    return df, missing

def merge(div, doe):
    colleges = div.merge(doe, on='WikidataID', how='left', suffixes=['', '_doe'])
    return colleges

if __name__ == "__main__":
    main()
