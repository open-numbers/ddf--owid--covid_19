# -*- coding: utf-8 -*-

import pandas as pd


source_file = '../source/owid-covid-data.csv'
codebook_file = '../source/owid-covid-codebook.csv'


def concept_id_to_name(s):
    return s.replace('_', ' ').title()


def main():
    codebook = pd.read_csv('../source/owid-covid-codebook.csv')
    df = pd.read_csv(source_file)
    # location entity domain
    locations = df[['iso_code', 'continent', 'location']].copy()
    locations.columns = ['iso_code', 'continent', 'name']
    locations['location'] = locations['iso_code'].str.lower()
    locations = locations.drop_duplicates()
    locations = locations.set_index('location').sort_index()
    locations.to_csv('../../ddf--entities--location.csv')

    # datapoints
    datapoints = df.drop(['continent', 'location'], axis=1).copy()
    datapoints['location'] = datapoints['iso_code'].str.lower()
    datapoints['date_'] = datapoints['date'].map(lambda x: x.replace('-', ''))
    datapoints = datapoints.drop(['iso_code', 'date'], axis=1)
    datapoints = datapoints.set_index(['location', 'date_'])
    datapoints.index.names = ['location', 'date']

    for c in datapoints.columns:
        fname = f'../../ddf--datapoints--{c}--by--location--date.csv'
        datapoints[c].dropna().to_csv(fname)

    # concepts
    codebook = pd.read_csv('../source/owid-covid-codebook.csv')
    concepts = codebook.copy()
    concepts = concepts.set_index('column')
    concepts['concept_type'] = 'measure'
    concepts.loc['location', 'concept_type'] = 'entity_domain'
    concepts.loc['date', 'concept_type'] = 'time'
    concepts['name'] = concepts.index.map(concept_id_to_name)
    concepts.loc['name', ['name', 'concept_type']] = ['Name', 'string']
    concepts.loc['category', ['name', 'concept_type']] = ['Category', 'string']
    concepts.loc['description', ['name', 'concept_type']] = ['Description', 'string']
    concepts.loc['source', ['name', 'concept_type']] = ['Source', 'string']
    concepts.loc['iso_code', 'concept_type'] = 'string'
    concepts.loc['continent', 'concept_type'] = 'string'
    concepts.index.name = 'concept'
    concepts.to_csv('../../ddf--concepts.csv')


if __name__ == '__main__':
    main()
    print('Done. Please consider updating datapackage.json')
