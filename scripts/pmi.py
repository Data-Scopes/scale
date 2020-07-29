from typing import Iterable, List, Union
from collections import Counter, OrderedDict
from itertools import combinations
import math


def count_tokens(token_sets: List[List[str]]) -> Counter:
    """Count items in set of item sets."""
    token_freq = Counter()
    for token_set in token_sets:
        token_freq.update(token_set)
    return token_freq


def count_token_cooc(token_sets: List[List[str]]) -> Counter:
    cooc_freq = Counter()
    for token_set in token_sets:
        cooc_freq.update([token_pair for token_pair in combinations(token_set, 2)])
    return cooc_freq


class PMICOOC(object):

    def __init__(self, token_sets: List[List[str]], filter_terms=Union[None, Iterable]):
        self.token_freq = count_tokens(token_sets)
        self.cooc_freq = count_token_cooc(token_sets)
        self.total_words = sum(self.token_freq.values())
        self.total_coocs = sum(self.cooc_freq.values())
        self.term_prob = {term: freq / self.total_words for term, freq in self.token_freq.items()}
        self.cooc_prob = {term_pair: freq / self.total_coocs for term_pair, freq in self.cooc_freq.items()}
        pmi = {}
        for term_pair, freq in self.cooc_freq.most_common():
            term1, term2 = term_pair
            if filter_terms and (term1 not in filter_terms or term2 not in filter_terms):
                continue
            pmi[term_pair] = math.log(self.cooc_prob[term_pair] / (self.term_prob[term1] * self.term_prob[term2]))
        self.pmi_cooc = OrderedDict(
            {term_pair: score for term_pair, score in sorted(pmi.items(), key=lambda x: x[1], reverse=True)})
        self.sorted_terms = list(self.pmi_cooc.keys())

    def __getitem__(self, item):
        return self.pmi_cooc[item] if item in self.pmi_cooc else self.sorted_terms[item]

    def items(self):
        return self.pmi_cooc.items()

    def highest(self, num: int) -> OrderedDict:
        highest = OrderedDict()
        for ki, key in enumerate(self.pmi_cooc):
            highest[key] = self.pmi_cooc[key]
            if ki == num:
                break
        return highest

