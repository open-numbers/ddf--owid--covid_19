# -*- coding: utf-8 -*-

from ddf_utils.factory.common import download

codebook_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-codebook.csv'
data_url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'


if __name__ == '__main__':
    download(codebook_url, '../source/owid-covid-codebook.csv')
    download(data_url, '../source/owid-covid-data.csv')
    print('done.')
