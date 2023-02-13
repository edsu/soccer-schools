#!/usr/bin/env python3

import time
import pandas
import requests
import reconciler

def main():
    df = get_divisions()
    df = reconcile(df)
    df = augment_wikidata(df)
    df = augment_doe(df)
    df.to_csv('data.csv', index=False)

def get_divisions():
    # Division 1
    d1 = pandas.read_csv('List_of_NCAA_Division_I_men%27s_soccer_programs_1.csv')
    d1 = d1[['Institution','Location','State', 'Conference']]
    d1.columns = ['School', 'City', 'State', 'Conference']
    d1['Division'] = 'D1'

    # Division 2
    d2 = pandas.read_csv('List_of_NCAA_Division_II_men%27s_soccer_programs_1.csv')
    d2 = d2[['School', 'City', 'State/Province', 'Conference']]
    d2.columns = ['School', 'City', 'State', 'Conference']
    d2['Division'] = 'D2'

    # Division 3
    d3 = pandas.read_csv('List_of_NCAA_Division_III_institutions_1.csv')
    d3 = d3[['School', 'City', 'State', 'Conference']]
    d3['Division'] = 'D3'

    # Join the divisions into one dataset
    df = pandas.concat([d1, d2, d3], ignore_index=True)

    # Remove newlines and abbreviations from the school name
    df['School'] = df['School'].str.replace(r' *\n *', ' ', regex=True)
    df['School'] = df['School'].str.replace(r' *\(.+\) *', '', regex=True)

    return df

def reconcile(df):
    # reconcile against Wikidata entities of type higher education institution
    recon = reconciler.reconcile(df['School'], type_id='Q38723')
    recon = recon[['id', 'input_value']]

    # merge the results, and drop/rename columns
    df = df.merge(recon, left_on='School', right_on='input_value', how='left')
    df = df.drop(['input_value'], axis=1)
    df = df.rename({'id': 'WikidataID'}, axis=1)
    df.to_csv('data.csv', index=False)

    # track wikidata misses
    missing = df[df['WikidataID'].isnull()]
    missing.to_csv('missing-wikidata.csv', index=False)
    df = df[~df['WikidataID'].isnull()]

    return df

def augment_wikidata(df):
    extra = pandas.DataFrame.from_records(df['WikidataID'].map(get_wikidata))
    df = df.merge(extra, on='WikidataID')
    df.to_csv('extra.csv', index=False)

    # track wikidata entities that lack postal code
    missing_zip = df[df['PostalCode'].isnull()]
    missing_zip.to_csv('missing-postalcode.csv', index=False)
    df = df[~df['PostalCode'].isnull()]

    return df

def augment_doe(df):
    doe = pandas.read_csv('Most-Recent-Cohorts-Institution.zip', low_memory=False)
    doe = doe[['INSTNM', 'ADM_RATE_ALL', 'SAT_AVG_ALL', 'COSTT4_A', 'ZIP']]
    doe.columns = ['School', 'AdmissionRate', 'SAT', 'Cost', 'PostalCode']

    doe = doe[~doe['PostalCode'].isnull()]

    df = df.merge(doe, on='PostalCode', how='left')
    return df

def get_wikidata(wikidata_id):
    """Get some extra data from Wikidata for a given Wikidata ID
    """
    time.sleep(.5)
    url = f"https://www.wikidata.org/w/rest.php/wikibase/v0/entities/items/{wikidata_id}/statements"
    data = requests.get(url).json()
    return {
        "WikidataID": wikidata_id,
        "PostalCode": pick(data, "P281"),
        "StudentCount": pick(data, "P2196"),
        "AdmissionRate": pick(data, "P5822"),
        "Location": pick(data, "P625")
    }

def pick(data, prop):
    """Get a Wikidata property value out of the Wikidata JSON
    """
    if prop in data and len(data[prop]) > 0:
        first = data[prop][0]
        prop_type = first["property"]["data-type"]
        if prop_type == "string":
            return first["value"]["content"]
        elif prop_type == "quantity":
            return first["value"]["content"]["amount"]
        elif prop_type == "globe-coordinate":
            content = first["value"]["content"]
            return f"{content['longitude']},{content['latitude']}"
    return None

if __name__ == "__main__":
    main()
