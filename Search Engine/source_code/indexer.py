# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:01:19 2020

@author: Sivaraman Lakshmipathy
"""

import os
import json
from text_processor import *
from logger_handler import *
from math import log, sqrt, pow
from persistence_handler import *

#Class to perform the indexing and construct the vector space retrieval model
class corpusHandler():
    term_frequency_key_df = "df"
    term_frequency_key_tf = "tf"

    def __init__(self, directory, persist_obj=None):
        custom_logger().log_message("Initializing Indexer component.", logger_handler.log_level_INFO)
        self.url_hash_map = {}
        self.term_frequency = {} #holds the term frequency for each token as token : {doc_count: count_val, tf:{doc_id: term_count}}
        self.doc_length = {} #holds the document lengths as {doc_id: doc_length}
        self.doc_count = 0
        if persist_obj is not None:
            self.persist_obj = persist_obj
        else:
            self.persist_obj = crawl_data_persistence_handler()
        self.collection_directory = directory

        self.text_processor = textProcessor()

        self.globalHandler()
        custom_logger().log_message("Exiting Indexer component.", logger_handler.log_level_INFO)

    def update_url_hash_map(self, hash, url):
        self.url_hash_map[hash] = url

    def get_url_for_hash(self, hash):
        if hash in self.url_hash_map:
            return self.url_hash_map[hash]

    def globalHandler(self):
        self.process_collection() #Build the inverted index
        self.generate_doc_length() #Calculate the document length for all documents

    def process_collection(self):
        collectionFiles = os.listdir(self.collection_directory)

        #Process files in the directory
        for entry in collectionFiles:
            cur_docid = entry
            cur_json = self.persist_obj.read(cur_docid)
            url = cur_json["url"].strip()
            self.update_url_hash_map(cur_docid, url)
            final_text = cur_json["content"].strip()
            self.build_term_frequency(self.text_processor.custom_tokenizer(final_text), cur_docid)
            self.doc_count += 1

    def generate_doc_length(self):
        collectionFiles = os.listdir(self.collection_directory)

        # Process files in the directory
        for entry in collectionFiles:
            cur_docid = entry
            cur_json = self.persist_obj.read(cur_docid)
            final_text = cur_json["content"].strip()
            sentence_tokens = set(self.text_processor.custom_tokenizer(final_text))
            sum = 0
            for token in sentence_tokens:
                try:
                    sum += pow(self.term_frequency[token][self.term_frequency_key_tf][cur_docid] * log((self.doc_count / self.term_frequency[token][self.term_frequency_key_df])), 2)
                except Exception as e:
                    custom_logger().log_message("Error constructing document length for token:" + token, logger_handler.log_level_WARNING)
            self.doc_length[cur_docid] = sqrt(sum)

    def build_term_frequency(self, sentence_tokens, fileId):
        for entry in sentence_tokens:
            if entry in self.term_frequency:
                entry_dict = self.term_frequency[entry]
                if fileId in entry_dict[self.term_frequency_key_tf]:
                    entry_dict[self.term_frequency_key_tf][fileId] += 1
                else:
                    entry_dict[self.term_frequency_key_tf][fileId] = 1
                    entry_dict[self.term_frequency_key_df] += 1
            else:
                self.term_frequency[entry] = {self.term_frequency_key_df: 1, self.term_frequency_key_tf: {fileId: 1}}

class indexer:
    pickle_file_name = os.path.dirname(os.getcwd()) + os.path.sep + "data" + os.path.sep + "indexer"

    def run_indexer(self):
        #invoke the inverted index based retrieval model generation and persistence
        corpus_indexer = corpusHandler(crawl_data_persistence_handler.data_dir)
        self.pickle_indexer(corpus_indexer)

    def pickle_indexer(self, pickle_object):
        pickle_handler.pickle_object(self.pickle_file_name, pickle_object)

    def unpickle_indexer(self):
        return pickle_handler.unpickle_object(self.pickle_file_name)
