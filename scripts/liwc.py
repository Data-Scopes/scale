from collections import defaultdict
import LIWCtools.LIWCtools as liwc_tools
import pandas as pd


class LIWC(object):

    def __init__(self, dict_filename: str):
        self.LD = liwc_tools.LDict(dict_filename, encoding='utf-8')
        self.liwc_cat = {}
        self.in_cat = defaultdict(lambda: defaultdict(bool))
        self.wildcard_word_prefix = defaultdict(lambda: defaultdict(bool))
        self.prefix_size = 2
        self.set_liwc_cat()

    def set_liwc_cat(self):
        for cat in self.LD.catDict.catDict:
            cat_dict = self.LD.catDict.catDict[cat]
            cat_dict_name, cat_dict_words = cat_dict
            self.liwc_cat[cat_dict_name] = cat_dict_words
            for word in cat_dict_words:
                if word.endswith('*'):
                    self.wildcard_word_prefix[word[:self.prefix_size]][word] = True
                    self.in_cat[word][cat_dict_name] = True
                else:
                    self.in_cat[word][cat_dict_name] = True

    def in_dict(self, word):
        if word in self.in_cat:
            return True
        elif word[:self.prefix_size] in self.wildcard_word_prefix:
            for wildcard_word in self.wildcard_word_prefix[word[:self.prefix_size]]:
                if word.startswith(wildcard_word):
                    return True
        return False

    def get_word_cats(self, word):
        return list(self.in_cat[word].keys())

    def has_categories(self, word):
        cats = []
        if word in self.in_cat:
            cats = self.get_word_cats(word)
        if word[:self.prefix_size] in self.wildcard_word_prefix:
            for wildcard_word in self.wildcard_word_prefix[word[:self.prefix_size]]:
                if word.startswith(wildcard_word[:-1]):
                    cats += self.get_word_cats(wildcard_word)
        return cats

    def text_dict_to_liwc_dataframe(self, text_dict):
        counts = {}
        for text_id in text_dict:
            counts[text_id] = self.LD.LDictCountString(text_dict[text_id])
        return pd.DataFrame(counts).transpose().fillna(0)
