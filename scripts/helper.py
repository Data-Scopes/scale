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


def get_doc_content_chunks(spacy_doc):
    """Get content chunks per sentence for all sentences in spacy_doc"""
    ncs_start_index = {nc.start: nc for nc in spacy_doc.noun_chunks}
    ncs_token_index = {t.i for nc in spacy_doc.noun_chunks for t in nc}
    for sent in spacy_doc.sents:
        yield get_sent_content_chunks(sent, ncs_start_index, ncs_token_index)


def get_sent_content_chunks(sent, ncs_start_index, ncs_token_index):
    """Get content chunks for a spacy sentence and a list of sentence noun chunks"""
    ordered_chunks = []
    for token in sent:
        if token.i in ncs_start_index:
            # if token is start element of noun_chunk, add whole noun_chunk to list
            ordered_chunks.append(ncs_start_index[token.i])
        elif token.i in ncs_token_index:
            # if token is non-start element of noun_chunk, skip it
            continue
        elif token.pos_ in ['VERB', 'ADJ', 'ADP', 'ADV'] and not token.is_stop:
            # if token is not part of a noun chunk and not a auxilliary or stop word, add it
            ordered_chunks.append(token)
    return ordered_chunks


def get_pmi_cooc(token_freq, cooc_freq, filter_terms=None):
    """Calculate pointwise mutual information for co-occurring terms."""
    total_words = sum(token_freq.values())
    total_coocs = sum(cooc_freq.values())
    term_prob = {term: freq / total_words for term, freq in token_freq.items()}
    cooc_prob = {term_pair: freq / total_coocs for term_pair, freq in cooc_freq.items()}
    pmi = {}
    for term_pair, freq in cooc_freq.most_common():
        term1, term2 = term_pair
        if filter_terms and (term1 not in filter_terms or term2 not in filter_terms):
            continue
        pmi[term_pair] = math.log(cooc_prob[term_pair] / (term_prob[term1] * term_prob[term2]))
    return OrderedDict({term_pair: score for term_pair, score in sorted(pmi.items(), key=lambda x: x[1], reverse=True)})


