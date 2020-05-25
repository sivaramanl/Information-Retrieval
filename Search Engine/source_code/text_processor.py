    # -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:01:19 2020

@author: Sivaraman Lakshmipathy
"""

import os
import sys
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

#Class to perform text processing operations
class textProcessor:
    stop_words = set(stopwords.words("english"))
    numbers = '0123456789'
    ps = PorterStemmer()

    def remove_punctuation_numbers(self, s):
        return ''.join(c for c in s if c not in punctuation)

    def tokenize_str(self, s):
        return word_tokenize(self.remove_punctuation_numbers(str.lower(s.strip())))

    def eliminate_stopwords(self, sentence_tokens):
        return [word for word in sentence_tokens if word not in self.stop_words]

    def perform_stemming(self, sentence_tokens):
        return [self.ps.stem(word) for word in sentence_tokens]

    def filter_minimumum_length(self, sentence_tokens, min_len=1):
        return [word for word in sentence_tokens if len(word) >= min_len]

    def custom_tokenizer(self, fileContent):
        sentence_tokens = self.tokenize_str(fileContent)
        sentence_tokens = self.eliminate_stopwords(sentence_tokens)
        sentence_tokens = self.perform_stemming(sentence_tokens)
        sentence_tokens = self.eliminate_stopwords(sentence_tokens)
        sentence_tokens = self.filter_minimumum_length(sentence_tokens)
        return sentence_tokens

    def get_int_from_str(self, str):
        temp = ''.join(c for c in str if c in self.numbers)
        if temp != '':
            return int(temp)
        return 0
