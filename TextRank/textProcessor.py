# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 18:10:04 2020

@author: Sivaraman Lakshmipathy
"""

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class textProcessor:
    stop_words = set(stopwords.words("english"))
    ps = PorterStemmer()

    def is_stop_word(self, target_word):
        return target_word in self.stop_words

    def get_stem(self, target_word):
        return self.ps.stem(target_word)

    def tokenize_str(self, s):
        return s.strip().split()
