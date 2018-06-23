import json
import csv
import os

from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from elasticsearch.helpers import streaming_bulk, parallel_bulk, reindex
from elasticsearch.exceptions import RequestError

es = Elasticsearch([os.enviorn['ES']])

def process_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['location'] = {'lat': row['latitude'], 'lon': row['longitude']}

            yield {
                '_op_index': 'index',
                '_index': 'acled_2018',
                '_type': 'event',
                '_id': int(row['data_id']),
                '_source': row
            }


if __name__ == '__main__':
    with open('./acled-template.json', 'r') as f:
        es.indices.put_template(name='acled', body=json.load(f))

    for ok, item in streaming_bulk(es, process_csv('acled_full.csv')):
        pass
