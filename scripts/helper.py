from typing import Iterator, Iterable, Tuple, Sized, Union
from elasticsearch import Elasticsearch
from collections import OrderedDict
import math
import numpy as np
import gzip
import json
import csv


def read_json(data_file: str) -> Iterator:
    """read_json reads the content of a JSON-line format file, which has a JSON document on each line.
    The gzip parameter can be used to read directly from gzipped files."""
    if data_file.endswith('.gz'):
        fh = gzip.open(data_file, 'rt')
    else:
        fh = open(data_file, 'rt')
    for line in fh:
        yield json.loads(line.strip())
    fh.close()


def read_csv(data_file: str) -> Iterator:
    """read_csv reads the content of a csv file. The gzip parameter can be used to read directly from gzipped files."""
    if data_file.endswith('.gz'):
        fh = gzip.open(data_file, 'rt')
    else:
        fh = open(data_file, 'rt')
    reader = csv.reader(fh, delimiter='\t')
    headers = next(reader)
    for row in reader:
        yield {header: row[hi] for hi, header in enumerate(headers)}
    fh.close()


def ecdf(data: Union[np.ndarray, Sized], reverse: bool = False) -> Tuple[Iterable, Iterable]:
    """Compute ECDF for a one-dimensional array of measurements.
    This function is copied from Eric Ma's tutorial on Bayes statistics at
    scipy 2019 https://github.com/ericmjl/bayesian-stats-modelling-tutorial"""
    # Number of data points
    n = len(data)
    # x-data for the ECDF
    x = np.sort(data)
    if reverse:
        x = np.flipud(x)
    # y-data for the ECDF
    y = np.arange(1, n+1) / n
    return x, y


def scroll_hits(es: Elasticsearch, query: dict, index: str, size: int = 100) -> iter:
    response = es.search(index=index, scroll='2m', size=size, body=query)
    sid = response['_scroll_id']
    scroll_size = response['hits']['total']
    print('total hits:', scroll_size)
    if type(scroll_size) == dict:
        scroll_size = scroll_size['value']
    # Start scrolling
    while scroll_size > 0:
        for hit in response['hits']['hits']:
            yield hit
        response = es.scroll(scroll_id=sid, scroll='2m')
        # Update the scroll ID
        sid = response['_scroll_id']
        # Get the number of results that we returned in the last scroll
        scroll_size = len(response['hits']['hits'])
        # Do something with the obtained page


