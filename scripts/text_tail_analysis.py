from typing import Dict, Iterable, Iterator, List, Set, Union
from collections import Counter, defaultdict
from spacy.tokens import Doc, DocBin, Span, Token
from pandas import DataFrame
import math
import time

from scripts.liwc import LIWC


def get_dataframe_review_texts(df: DataFrame) -> Iterator[str]:
    """return the review texts from a sample dataframe."""
    num_rows = len(df)
    review_text_col = list(df.columns).index('review_text')
    for row_num in range(0, num_rows):
        yield df.iloc[row_num, review_text_col]


def get_doc_content_chunks(spacy_doc: Doc) -> Iterator[List[Union[Token, Span]]]:
    """Get content chunks per sentence for all sentences in spacy_doc"""
    ncs_start_index = {nc.start: nc for nc in spacy_doc.noun_chunks}
    ncs_token_index = {t.i for nc in spacy_doc.noun_chunks for t in nc}
    for sent in spacy_doc.sents:
        yield get_sent_content_chunks(sent, ncs_start_index, ncs_token_index)


def get_sent_content_chunks(sent: Span, ncs_start_index: Dict[int, Span],
                            ncs_token_index: Set[int]) -> List[Union[Token, Span]]:
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


def get_word_tokens(doc: Doc) -> List[Token]:
    """Return only tokens that are not stopwords and not punctuation."""
    return [token for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]


def get_doc_word_token_set(doc: Doc, use_lemma=False) -> Set[Token]:
    """Return the set of tokens in a document (no repetition)."""
    return set([token.lemma_ if use_lemma else token.text for token in get_word_tokens(doc)])


def filter_pos(tokens: Iterable[Token], include_pos: List[str]):
    """Filter tokens based a list of POS tags"""
    return [token for token in tokens if token.pos_ in include_pos]


def get_lemmas(tokens: Iterable[Token]):
    return [token.text if token.pos_ == 'PRON' else token.lemma_ for token in tokens]


def get_lemma_pos(tokens: Iterable[Token], keep_pron: bool = False):
    """Iterate over a set of tokens and return tuples of lemma and POS."""
    if keep_pron:
        return [(token.text, token.pos_) if token.pos_ == 'PRON' else (token.lemma_, token.pos_) for token in tokens]
    else:
        return [(token.lemma_, token.pos_) for token in tokens]


def has_lemma_pos(token_iter: Iterable[Token], lemma: str, pos: str) -> bool:
    for token in token_iter:
        if token.lemma_ == lemma and token.pos_ == pos:
            return True
    return False


def sentence_iter(docs: List[Doc]):
    """Iterate over a list of spacy docs and return individual sentences."""
    for doc in docs:
        for sent in doc.sents:
            yield sent


def get_lemma_pos_tf_index(docs: List[Doc], keep_pron: bool = False) -> Counter:
    """Iterate over all tokens in a set of spacy docs and index the frequency of a token's lemma and POS."""
    tf_lemma_pos = Counter()
    for doc in docs:
        tf_lemma_pos.update(get_lemma_pos(doc, keep_pron=keep_pron))
    return tf_lemma_pos


def get_lemma_pos_df_index(docs: List[Doc], keep_pron: bool = False) -> Counter:
    """Iterate over all tokens in a set of spacy docs and index the document frequency of a token's lemma and POS."""
    df_lemma_pos = Counter()
    for doc in docs:
        df_lemma_pos.update(get_lemma_pos(get_doc_word_token_set(doc), keep_pron=keep_pron))
    return df_lemma_pos


def show_tail_lemmas(tf_lemma_pos: Counter, tf_threshold: int = 1, pos: str = None, num_lemmas: int = 100):
    """Print lemmas below a certain TF threshold. Optionally, add a POS filter to only
    see lemmas with a specific part-of-speech."""
    if pos:
        lemmas = [lemma for lemma, pos in tf_lemma_pos if tf_lemma_pos[(lemma, pos)] == tf_threshold and pos == pos]
    else:
        lemmas = [lemma for lemma, pos in tf_lemma_pos if tf_lemma_pos[(lemma, pos)] == tf_threshold]
    for i in range(0, 100, 5):
        print(''.join([f'{lemmas[j]: <16}' for j in range(i, i + 5)]))


def show_pos_tail_distribution(tf_lemma_pos):
    all_pos = defaultdict(int)
    low_pos = defaultdict(int)
    one_pos = defaultdict(int)
    for lemma, pos in tf_lemma_pos:
        all_pos[pos] += tf_lemma_pos[(lemma, pos)]
        if tf_lemma_pos[(lemma, pos)] <= 5:
            low_pos[pos] += tf_lemma_pos[(lemma, pos)]
        if tf_lemma_pos[(lemma, pos)] == 1:
            one_pos[pos] += tf_lemma_pos[(lemma, pos)]

    print('Word form\tAll TF (frac)\tTF <= 5 (frac)\tTF = 1 (frac)')
    print('------------------------------------------------------------')
    for pos in all_pos:
        all_frac = round(all_pos[pos] / sum(all_pos.values()), 2)
        low_frac = round(low_pos[pos] / sum(low_pos.values()), 2)
        one_frac = round(one_pos[pos] / sum(one_pos.values()), 2)
        all_pos_string = f'\t{all_pos[pos]: > 8}{all_frac: >6.2f}'
        low_pos_string = f'\t{low_pos[pos]: >6}{low_frac: >6.2}'
        one_pos_string = f'\t{one_pos[pos]: >6}{one_frac: >6.2}'
        print(f'{pos: <10}{all_pos_string}{low_pos_string}{one_pos_string}')


def group_by_head(docs: List[Doc], tf_lemma_pos: Counter, token_pos_types: List[str],
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


def group_by_child(docs: List[Doc], tf_lemma_pos: Counter, token_pos_types: List[str],
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


attrs = [
    "IS_ALPHA", "IS_PUNCT", "IS_STOP", "IS_SPACE",
    "LENGTH", "LEMMA", "POS", "TAG", "DEP",
    "ENT_IOB", "ENT_TYPE", #"ENT_ID", "ENT_KB_ID",
    "HEAD", "SENT_END", #"SPACY", "PROB", "LANG",
    "IDX",
]


def read_doc_bin(fname: str) -> DocBin:
    with open(fname, 'rb') as fh:
        doc_bin_bytes = fh.read()
        return DocBin().from_bytes(doc_bin_bytes)


def read_docs_from_bin(fname: str, nlp) -> List[Doc]:
    doc_bin = read_doc_bin(fname)
    return list(doc_bin.get_docs(nlp.vocab))


def write_docs_to_bin(docs: List[Doc], fname: str) -> None:
    doc_bin = DocBin(attrs=attrs)
    for doc in docs:
        doc_bin.add(doc)
    with open(fname, 'wb') as fh:
        doc_bin_bytes = doc_bin.to_bytes()
        fh.write(doc_bin_bytes)


def spacy_parse_store_from_dataframe(fname, df, nlp):
    chunks = math.ceil(len(df))
    start_time = time.time()
    for chunk in range(chunks):
        start = chunk * 10000
        end = start + 10000
        chunk_df = df.iloc[start:end, ]
        chunk_fname = fname + f'_{chunk}'
        doc_bin = DocBin(attrs=attrs)
        for ti, text in enumerate(get_dataframe_review_texts(chunk_df)):
            doc = nlp(text)
            doc_bin.add(doc)
            if (ti+1) % 1000 == 0:
                print(ti+1, 'reviews parsed in chunk', chunk, '\ttime:', time.time() - start_time)
        with open(chunk_fname, 'wb') as fh:
            fh.write(doc_bin.to_bytes())


def read_spacy_docs_for_dataframe(fname, df, nlp):
    docs = read_docs_from_bin(fname, nlp)
    return add_review_id_to_spacy_docs(df, docs)


def add_review_id_to_spacy_docs(df, docs):
    if len(df) != len(docs):
        raise IndexError('dataframe and spacy docs list are not the same length!')
    review_ids = list(df.review_id)
    return {review_id: docs[ri] for ri, review_id in enumerate(review_ids)}


def select_dataframe_spacy_docs(df, docs_dict, as_dict=False):
    review_ids = set(list(df.review_id))
    if as_dict:
        return {review_id: docs_dict[review_id] for review_id in review_ids if review_id in review_ids}
    else:
        return [docs_dict[review_id] for review_id in review_ids if review_id in review_ids]


def add_data(data, tf_lemma_pos, dep_type, dep_lemma_pos, tail_lemma_pos, dep_tail_count, cat):
    dep_lemma, dep_pos = dep_lemma_pos
    tail_lemma, tail_pos = tail_lemma_pos
    data['dependency_type'] += [dep_type]
    data['dependency_word'] += [dep_lemma]
    data['dependency_pos'] += [dep_pos]
    data['dependency_freq'] += [tf_lemma_pos[dep_lemma_pos]]
    data['tail_word'] += [tail_lemma]
    data['tail_pos'] += [tail_pos]
    data['tail_freq'] += [tf_lemma_pos[tail_lemma_pos]]
    data['dep_tail_freq'] += [dep_tail_count]
    data['liwc_category'] += [cat]


def get_tail_groupings(doc_list, tf_lemma_pos, token_pos_types, liwc, max_threshold=5, min_threshold=0):
    tail_groupings = {'dependency_type': [], 'dependency_word': [], 'dependency_pos': [], 'dependency_freq': [],
                      'tail_word': [], 'tail_pos': [], 'tail_freq': [],
                      'dep_tail_freq': [], 'liwc_category': []}

    dep_groups = {
        'head': group_by_head(doc_list, tf_lemma_pos, token_pos_types,
                              max_threshold=max_threshold, min_threshold=min_threshold),
        'child': group_by_child(doc_list, tf_lemma_pos, token_pos_types,
                                max_threshold=max_threshold, min_threshold=min_threshold)
    }
    for dep_type in dep_groups:
        for dep_lemma_pos in dep_groups[dep_type]:
            if len(dep_groups[dep_type][dep_lemma_pos]) < 1:
                continue
            dep_lemma, dep_pos = dep_lemma_pos
            for tail_lemma_pos in dep_groups[dep_type][dep_lemma_pos]:
                dep_tail_count = dep_groups[dep_type][dep_lemma_pos][tail_lemma_pos]
                tail_lemma, tail_pos = tail_lemma_pos
                if not liwc.in_dict(tail_lemma):
                    cat = None
                else:
                    cat = "|".join(liwc.has_categories(tail_lemma))
                add_data(tail_groupings, tf_lemma_pos, dep_type, dep_lemma_pos,
                         tail_lemma_pos, dep_tail_count, cat)
    return tail_groupings
