# -*- coding: utf-8 -*-
"""
Created on Wed Feb 05 14:10:24 2020

@author: Sivaraman Lakshmipathy
"""

import os
import sys
from string import punctuation
from zipfile import ZipFile
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from math import log, sqrt, pow


class textProcessor:
    stop_words = set(stopwords.words("english"))
    numbers = '0123456789'
    ps = PorterStemmer()

    def remove_punctuation_numbers(self, s):
        return ''.join(c for c in s if c not in punctuation and c not in self.numbers)

    def tokenize_str(self, s):
        return word_tokenize(self.remove_punctuation_numbers(str.lower(s.strip())))

    def eliminate_stopwords(self, sentence_tokens):
        return [word for word in sentence_tokens if word not in self.stop_words]

    def perform_stemming(self, sentence_tokens):
        return [self.ps.stem(word) for word in sentence_tokens]

    def filter_minimumum_length(self, sentence_tokens, min_len = 3):
        return [word for word in sentence_tokens if len(word)>= min_len]

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

class corpusHandler(textProcessor):
    term_frequency_key_df = "df"
    term_frequency_key_tf = "tf"

    def __init__(self, directory):
        self.collection_directory = directory
        self.term_frequency = {} #holds the term frequency for each token as token : {doc_count: count_val, tf:{doc_id: term_count}}
        self.doc_length = {} #holds the document lengths as {doc_id: doc_length}
        self.collection_size = 0
        self.doc_count = 0

        self.globalHandler()

    def globalHandler(self):
        self.process_collection()
        self.generate_doc_length()

    def process_collection(self):
        collectionFiles = os.listdir(self.collection_directory)

        #Process files in the directory
        for entry in collectionFiles:
            cur_file_path = self.collection_directory + os.path.sep + entry
            cur_docid = self.get_int_from_str(entry)
            with open(cur_file_path, "r") as f:
                cur_text = f.read()
                soup_text = BeautifulSoup(cur_text, 'lxml')
                title_text = soup_text.find('title').get_text().strip()
                text_text = soup_text.find('text').get_text()
                final_text = (title_text + text_text).strip()
                self.build_term_frequency(self.custom_tokenizer(final_text), cur_docid)
                self.doc_count += 1

    def generate_doc_length(self):
        collectionFiles = os.listdir(self.collection_directory)

        # Process files in the directory
        for entry in collectionFiles:
            cur_file_path = self.collection_directory + os.path.sep + entry
            cur_docid = self.get_int_from_str(entry)
            with open(cur_file_path, "r") as f:
                cur_text = f.read()
                soup_text = BeautifulSoup(cur_text, 'lxml')
                title_text = soup_text.find('title').get_text().strip()
                text_text = soup_text.find('text').get_text()
                final_text = (title_text + text_text).strip()
                sentence_tokens = set(self.custom_tokenizer(final_text))

                sum = 0
                for token in sentence_tokens:
                    try:
                        sum += pow(self.term_frequency[token][self.term_frequency_key_tf][cur_docid] * log((self.doc_count / self.term_frequency[token][self.term_frequency_key_df])), 2)
                    except Exception as e:
                        print("Error", token)
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

class queryHandler(textProcessor):
    ranks = [10, 50, 100, 500]
    metrics_key_precision = 'p'
    metrics_key_recall = 'r'

    def __init__(self, filePath, relevanceFilePath, corpusObj):
        self.queryFile = filePath
        self.relevance_map = self.readRelevance(relevanceFilePath)
        self.process_queries(corpusObj)

    def readRelevance(self, filePath):
        relevance_map = {}
        with open(filePath, "r") as f:
            for entry in f:
                query_id, relevant_doc_id = entry.strip().split()
                query_id = int(query_id)
                relevant_doc_id = int(relevant_doc_id)
                if query_id in relevance_map:
                    relevance_map[query_id].add(relevant_doc_id)
                else:
                    relevance_map[query_id] = {relevant_doc_id}
        return relevance_map

    def process_queries(self, corpus_obj):
        with open(self.queryFile, "r") as f:
            temp = f.read()
            queries = temp.split("\n")

        metrics_map = {}
        cur_queryid = 1
        for query in queries:
            cosine_sim_map = self.generate_cosine_similarity(query, corpus_obj)
            cosine_sim_map = {k: v for k, v in sorted(cosine_sim_map.items(), key=lambda item: item[1], reverse=True)}
            metrics_map[cur_queryid] = self.calculate_metrics(cosine_sim_map, self.ranks, self.relevance_map[cur_queryid])
            cur_queryid += 1

        self.pretty_print(metrics_map, self.ranks)

    def pretty_print(self, metrics_map, ranks):
        for rank in ranks:
            tot_p, tot_r, counter = 0, 0, 0
            print("Top", rank, "documents in rank list")
            for queryid, metrics in metrics_map.items():
                cur_p = metrics[rank][self.metrics_key_precision]
                cur_r = metrics[rank][self.metrics_key_recall]
                tot_p += cur_p
                tot_r += cur_r
                counter += 1
                print("Query: ", queryid, "\tPr: ", cur_p, "\tRe: ", cur_r)
            print()
            print()
            print("Avg precision:", tot_p/counter)
            print("Avg recall:", tot_r/counter)
            print()

    def calculate_metrics(self, cosine_sim_map, ranks, relevant_docs):
        relevant_docs_len = len(relevant_docs)
        max_rank = max(ranks)
        cur_relevant_docs_len = 0
        counter = 0
        metrics_map = {}
        for entry, val in cosine_sim_map.items():
            counter += 1
            if entry in relevant_docs:
                cur_relevant_docs_len += 1
            if counter in ranks:
                cur_precision = cur_relevant_docs_len / counter
                cur_recall = cur_relevant_docs_len / relevant_docs_len
                metrics_map[counter] = {self.metrics_key_precision: cur_precision, self.metrics_key_recall: cur_recall}
            if counter >= max_rank:
                break
        return metrics_map

    def generate_cosine_similarity(self, query, corpus_obj):
        query_tokens = self.custom_tokenizer(query)

        cosine_sim_map = {}
        for token in query_tokens:
            if token in corpus_obj.term_frequency:
                token_obj = corpus_obj.term_frequency[token]
                token_doc_freq = token_obj[corpus_obj.term_frequency_key_df]
                token_term_freq = token_obj[corpus_obj.term_frequency_key_tf]

                for docid, tf in token_term_freq.items():
                    cur_cosine_sim = (1 * log (corpus_obj.doc_count / token_doc_freq)) * (tf * log(corpus_obj.doc_count / token_doc_freq))
                    if docid in cosine_sim_map:
                        cosine_sim_map[docid] += cur_cosine_sim
                    else:
                        cosine_sim_map[docid] = cur_cosine_sim

        for docid in cosine_sim_map.keys():
            cosine_sim_map[docid] /= corpus_obj.doc_length[docid]

        return cosine_sim_map


def extract_files(zip_file_full_path):
    if os.path.exists(zip_file_full_path):
        with ZipFile(zip_file_full_path, 'r') as f:
            f.extractall()

def main():
    data_collection_zip_file = "cranfield.tar.gz"
    data_collection_directory = "cranfieldDocs"
    query_file = "queries.txt"
    relevance_file = "relevance.txt"
    try:
        if len(sys.argv) >= 3:
            query_file = sys.argv[1]
            relevance_file = sys.argv[2]
            if len(sys.argv) >= 4:
                data_collection_directory = sys.argv[3]
                if len(sys.argv) == 5:
                    data_collection_zip_file = sys.argv[3]
                    data_collection_directory = sys.argv[4]
                else:
                    data_collection_zip_file = None
        else:
            print("Insufficient input parameters. Reverting to default files.")
    except Exception as e:
        query_file = "queries.txt"
        relevance_file = "relevance.txt"
        data_collection_zip_file = "cranfield.tar.gz"
        data_collection_directory = "cranfieldDocs"
    if not os.path.exists(query_file):
        print("Query file not found. Exiting.")
        return
    if not os.path.exists(relevance_file):
        print("Relevance file not found. Exiting.")
        return
    if not os.path.exists(data_collection_directory) and data_collection_zip_file is not None:
        extract_files(data_collection_zip_file)
    if not os.path.exists(data_collection_directory) or not os.path.isdir(data_collection_directory):
        print("Directory to be processed not found. Exiting.")
        return

    print("Evaluating your queries...")
    corpus_obj = corpusHandler(data_collection_directory)

    queryHandler(query_file, relevance_file, corpus_obj)

if __name__ == "__main__":
    main()