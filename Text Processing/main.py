# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 18:40:46 2020

@author: Sivaraman Lakshmipathy
"""

import os
import sys
from string import punctuation
from zipfile import ZipFile
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class textProcessor():

    def __init__(self, collection_directory, stemmer_enabled = False, eliminate_stop_words = False):
        self.collection_directory = collection_directory
        self.term_frequency = {}
        self.collection_size = 0
        self.stop_words = set(stopwords.words("english"))
        self.stemmer_enabled = stemmer_enabled
        self.eliminate_stop_words = eliminate_stop_words

    def process_collection(self):
        collectionFiles = os.listdir(self.collection_directory)

        #Process files in the directory
        for entry in collectionFiles:
            cur_file_path = self.collection_directory + os.path.sep + entry
            with open(cur_file_path, "r") as f:
                cur_text = f.readlines()
                for entry in cur_text:
                    self.preprocessor(entry)

        #Sort term frequency in descending order
        self.term_frequency = {k: v for k, v in sorted(self.term_frequency.items(), key=lambda item: item[1], reverse=True)}

    def total_count(self):
        print("Total number of words in the collection:", self.collection_size)

    def print_vocab_size(self):
        print("Vocabulary size:", len(self.term_frequency.keys()))

    def top_N_keys(self, n, only_stop_words = False):
        i = 0
        if only_stop_words:
            if self.eliminate_stop_words:
                print("Stop words in top {} words in the collection:".format(n), " <<No stop words available>>\n")
                return
            else:
                print("Stop words in top {} words in the collection:".format(n))
        else:
            print("\nTop {} words in the collection:".format(n))
        for key, value in self.term_frequency.items():
            if not only_stop_words or (only_stop_words and key in self.stop_words):
                print(key, "\t", value)
            i += 1
            if i >= n:
                break
        print("")

    def top_percentage_counter(self, n):
        sum = 0
        i = 0
        for key, value in self.term_frequency.items():
            sum += value
            i += 1
            if (sum / self.collection_size * 100) >= n:
                break
        print("Minimum number of unique words accounting for {}% of total number of words in the collection: {}".format(n, i))
        return i

    def print_stats(self):
        self.total_count()
        self.print_vocab_size()
        self.top_N_keys(20)
        self.top_N_keys(20, True)
        count_val = self.top_percentage_counter(15)
        self.top_N_keys(count_val)

    def remove_punctuation(self, s):
        return ''.join(c for c in s if c not in punctuation)

    def tokenize_str(self, s):
        return word_tokenize(self.remove_punctuation(str.lower(s.strip())))

    def preprocessor(self, entry):
        sentence_tokens = self.tokenize_str(entry)

        if self.eliminate_stop_words:
            sentence_tokens = [word for word in sentence_tokens if word not in self.stop_words]

        if self.stemmer_enabled:
            ps = PorterStemmer()
            sentence_tokens = [ps.stem(word) for word in sentence_tokens]

        #Update colletion word count
        self.collection_size += len(sentence_tokens)

        #Update term frequency
        token_frequency = dict(FreqDist(sentence_tokens))
        for key, value in token_frequency.items():
            if key in self.term_frequency:
                self.term_frequency[key] += value
            else:
                self.term_frequency[key] = value

def extract_files(zip_file_full_path):
    if os.path.exists(zip_file_full_path):
        with ZipFile(zip_file_full_path, 'r') as f:
            f.extractall()

def main():
    data_collection_zip_file = "citeseer.zip"
    data_collection_directory = "citeseer"
    try:
        if len(sys.argv) == 2:
            data_collection_directory = sys.argv[1]
            data_collection_zip_file = None
        elif len(sys.argv) == 3:
            data_collection_zip_file = sys.argv[1]
            data_collection_directory = sys.argv[2]
    except Exception as e:
        data_collection_zip_file = "citeseer.zip"
        data_collection_directory = "citeseer"
    if not os.path.exists(data_collection_directory) and data_collection_zip_file is not None:
        extract_files(data_collection_zip_file)
    if not os.path.exists(data_collection_directory) or not os.path.isdir(data_collection_directory):
        print("Directory to be processed not found. Exiting.")
        return

    print("Text processing WITHOUT Stemming and stop word removal")
    text_processor_obj = textProcessor(data_collection_directory)
    text_processor_obj.process_collection()
    text_processor_obj.print_stats()

    print("")
    print("Text processing WITH Stemming and stop word removal")
    text_processor_obj2 = textProcessor(data_collection_directory, True, True)
    text_processor_obj2.process_collection()
    text_processor_obj2.print_stats()

if __name__ == "__main__":
    main()
