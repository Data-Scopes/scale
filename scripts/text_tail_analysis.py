from typing import List, Union
from collections import Counter, defaultdict


def filter_pos(tokens, include_pos: List[str]):
    """Filter tokens based a list of POS tags"""
    return [token for token in tokens if token.pos_ in include_pos]


def get_lemmas(tokens):
    return [token.text if token.pos_ == 'PRON' else token.lemma_ for token in tokens]


def get_lemma_pos(tokens):
    """Iterate over a set of tokens and return tuples of lemma and POS."""
    return [(token.lemma_, token.pos_) for token in tokens]


def sentence_iter(docs):
    """Iterate over a list of spacy docs and return individual sentences."""
    for doc in docs:
        for sent in doc.sents:
            yield sent


def get_lemma_pos_tf_index(docs):
    """Iterate over all tokens in a set of spacy docs and index the frequency of a token's lemma and POS."""
    tf_lemma_pos = Counter()
    for doc in docs:
        tf_lemma_pos.update(get_lemma_pos(doc))
    return tf_lemma_pos


def group_by_head(docs, tf_lemma_pos: Counter, token_pos_types: List[str],
                  head_pos_types: List[str] = ['ADJ', 'ADV', 'NOUN', 'PROPN', 'VERB'],
                  max_threshold: Union[None, int] = None, min_threshold: Union[None, int] = None):
    """Iterate over a set of spacy docs and group all terms within a frequency threshold by their head term.
    The head term is based on the Spacy dependency parse."""
    head_group = defaultdict(Counter)
    for sent in sentence_iter(docs):
        for token in sent:
            # skip tokens with a POS that is not in the accepted token POS list
            if token.pos_ not in token_pos_types:
                continue
            token_lemma_pos = (token.lemma_, token.pos_)
            # skip if the token's lemma+POS is outside optional frequency thresholds
            if max_threshold and token_lemma_pos in tf_lemma_pos and tf_lemma_pos[token_lemma_pos] > max_threshold:
                continue
            if min_threshold and token_lemma_pos in tf_lemma_pos and tf_lemma_pos[token_lemma_pos] < min_threshold:
                continue
            # skip if head POS is not in the accepted head POS list
            if token.head.pos_ not in head_pos_types:
                continue
            head_lemma_pos = (token.head.lemma_, token.head.pos_)
            head_group[head_lemma_pos].update([token_lemma_pos])
    return head_group


def group_by_child(docs, tf_lemma_pos: Counter, token_pos_types: List[str],
                   child_pos_types: List[str] = ['ADJ', 'ADV', 'NOUN', 'PROPN', 'VERB'],
                   max_threshold: Union[None, str] = None, min_threshold: Union[None, int] = None):
    """Iterate over a set of spacy docs and group all terms within a frequency threshold by their head term.
    The head term is based on the Spacy dependency parse."""
    child_group = defaultdict(Counter)
    for sent in sentence_iter(docs):
        for token in sent:
            # skip tokens with a POS that is not in the accepted token POS list
            if token.pos_ not in token_pos_types:
                continue
            token_lemma_pos = (token.lemma_, token.pos_)
            # skip if the token's lemma+POS is outside optional frequency thresholds
            if max_threshold and token_lemma_pos in tf_lemma_pos and tf_lemma_pos[token_lemma_pos] > max_threshold:
                continue
            if min_threshold and token_lemma_pos in tf_lemma_pos and tf_lemma_pos[token_lemma_pos] < min_threshold:
                continue
            # skip if child POS is not in the accepted child POS list
            for child in token.children:
                if child.pos_ not in child_pos_types:
                    continue
                child_lemma_pos = (child.lemma_, child.pos_)
                child_group[child_lemma_pos].update([token_lemma_pos])
    return child_group
