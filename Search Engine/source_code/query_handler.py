# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:01:19 2020

@author: Sivaraman Lakshmipathy
"""

from text_processor import *
from logger_handler import *
from math import log, sqrt, pow

#Class to handle input query and retrieve search results
class query_handler():
    similarity_measures = ["Inner Product", "Dice coefficient", "Cosine similarity", "Jaccard coefficient"]

    def __init__(self, corpus_obj, network_graph, lda_obj):
        self.query = None
        self.cached_results = None #Cache the results for pagination
        self.cached_results_expanded = None #Cache the results for pagination
        self.navigator_start = 0
        self.navigator_page_size = 10
        self.corpus_obj = corpus_obj
        self.graph = network_graph
        self.lda_obj = lda_obj
        self.text_processor = textProcessor()

    def clear_cache(self):
        #Clear the cached results
        self.cached_results = None
        self.cached_results_expanded = None
        self.navigator_start = 0

    def getResults(self, query, sim_measure):
        try:
            if sim_measure not in range(1, len(self.similarity_measures)+1):
                #default similarity measure is Cosine Similarity
                sim_measure = 3
            self.clear_cache()
            custom_logger().log_message("Query:" + query, logger_handler.log_level_INFO) #Record the query

            #Retrieve the relevant documents
            if sim_measure == 1:
                self.generate_inner_product_similarity(query)
            elif sim_measure == 2:
                self.generate_dice_similarity(query)
            elif sim_measure == 4:
                self.generate_jaccard_similarity(query)
            else:
                self.generate_cosine_similarity(query)

            #Rank the retrieved results
            self.rank_results()
            self.navigator_start = 0
        except Exception as e:
            custom_logger().log_message("Exception while processing query: " + query + "\n" + str(e), logger_handler.log_level_CRITICAL)

        #Generate the final results
        return self.get_resultset()

    def get_previous_resultset(self):
        #Pagination: Retrieve previous set of results for the same query
        temp = self.navigator_start
        self.navigator_start -= self.navigator_page_size
        if self.navigator_start < 0:
            self.navigator_start = temp
        return self.get_resultset()

    def get_next_resultset(self):
        # Pagination: Retrieve next set of results for the same query
        temp = self.navigator_start
        self.navigator_start += self.navigator_page_size
        if self.navigator_start > max(len(self.cached_results), len(self.cached_results_expanded)):
            self.navigator_start = temp
        return self.get_resultset()

    def get_resultset(self):
        result_set = []
        result_set_expanded = []
        if self.cached_results is None and self.cached_results_expanded is None:
            return [], [], False, False

        #Fetch subset of results and rank the results based on pagerank scores
        if self.navigator_start <= len(self.cached_results):
            result_set = list(self.cached_results.keys())[self.navigator_start: self.navigator_start + self.navigator_page_size]
            result_set = sorted(result_set, key=lambda item_1: self.harmonic_mean(self.cached_results, item_1), reverse=True)
            result_set = [self.corpus_obj.url_hash_map[item] for item in result_set]

        if self.navigator_start <= len(self.cached_results_expanded):
            result_set_expanded = list(self.cached_results_expanded.keys())[self.navigator_start: self.navigator_start + self.navigator_page_size]
            result_set_expanded = sorted(result_set_expanded, key=lambda item_2: self.harmonic_mean(self.cached_results_expanded, item_2), reverse=True)
            result_set_expanded = [self.corpus_obj.url_hash_map[item] for item in result_set_expanded]

        #Pagination
        max_len = max(len(self.cached_results), len(self.cached_results_expanded))

        can_next = True
        can_prev = True
        if self.navigator_start + self.navigator_page_size >= max_len:
            can_next = False
        if self.navigator_start - self.navigator_page_size < 0:
            can_prev = False
        return result_set, result_set_expanded, can_next, can_prev

    #General method to calculate the similarity score
    def generate_similarity_measure(self, query, expand=False):
        query_tokens = self.text_processor.custom_tokenizer(query)
        if expand:
            expanded_query = self.lda_obj.get_related_words(query)
            for new_term in expanded_query:
                if new_term not in query_tokens:
                    query_tokens.extend([new_term])
            custom_logger().log_message("Expanded query:" + " ".join(str(item) for item in query_tokens), logger_handler.log_level_INFO)

        similarity_map = {}
        query_length = {}
        for token in query_tokens:
            if token in self.corpus_obj.term_frequency:
                token_obj = self.corpus_obj.term_frequency[token]
                token_doc_freq = token_obj[self.corpus_obj.term_frequency_key_df]
                token_term_freq = token_obj[self.corpus_obj.term_frequency_key_tf]

                for docid, tf in token_term_freq.items():
                    token_weight = (1 * log(self.corpus_obj.doc_count / token_doc_freq))
                    cur_cosine_sim = token_weight * (tf * log(self.corpus_obj.doc_count / token_doc_freq))
                    if docid in similarity_map:
                        similarity_map[docid] += cur_cosine_sim
                    else:
                        similarity_map[docid] = cur_cosine_sim
                    if docid in query_length:
                        query_length[docid] += pow(token_weight, 2)
                    else:
                        query_length[docid] = pow(token_weight, 2)
        return similarity_map, query_length

    def generate_inner_product_similarity(self, query):
        inner_product_map, _ = self.generate_similarity_measure(query)
        self.cached_results = inner_product_map
        inner_product_map_2, _ = self.generate_similarity_measure(query, True)
        self.cached_results_expanded = inner_product_map_2

    def generate_dice_similarity(self, query):
        dice_similarity_map, query_length = self.generate_similarity_measure(query)
        for docid in dice_similarity_map.keys():
            dice_similarity_map[docid] = (2 * dice_similarity_map[docid]) / (pow(self.corpus_obj.doc_length[docid], 2) + query_length[docid])
        self.cached_results = dice_similarity_map
        dice_similarity_map_2, query_length = self.generate_similarity_measure(query, True)
        for docid in dice_similarity_map_2.keys():
            dice_similarity_map_2[docid] = (2 * dice_similarity_map_2[docid]) / (pow(self.corpus_obj.doc_length[docid], 2) + query_length[docid])
        self.cached_results_expanded = dice_similarity_map_2

    def generate_cosine_similarity(self, query):
        cosine_sim_map, _ = self.generate_similarity_measure(query)
        for docid in cosine_sim_map.keys():
            cosine_sim_map[docid] /= self.corpus_obj.doc_length[docid]
        self.cached_results = cosine_sim_map
        cosine_sim_map_2, _ = self.generate_similarity_measure(query, True)
        for docid in cosine_sim_map_2.keys():
            cosine_sim_map_2[docid] /= self.corpus_obj.doc_length[docid]
        self.cached_results_expanded = cosine_sim_map_2

    def generate_jaccard_similarity(self, query):
        jaccard_similarity_map, query_length = self.generate_similarity_measure(query)
        for docid in jaccard_similarity_map.keys():
            jaccard_similarity_map[docid] = (jaccard_similarity_map[docid]) / (pow(self.corpus_obj.doc_length[docid], 2) + query_length[docid] - jaccard_similarity_map[docid])
        self.cached_results = jaccard_similarity_map
        jaccard_similarity_map_2, query_length = self.generate_similarity_measure(query)
        for docid in jaccard_similarity_map_2.keys():
            jaccard_similarity_map_2[docid] = (jaccard_similarity_map_2[docid]) / (pow(self.corpus_obj.doc_length[docid], 2) + query_length[docid] - jaccard_similarity_map_2[docid])
        self.cached_results_expanded = jaccard_similarity_map_2

    #Harmonic mean to calculate scores based on similarity score and pagerank score
    def harmonic_mean(self, score_obj, key):
        pg_score = self.graph.get_node_score(key)
        return (2 * score_obj[key] * pg_score) / (score_obj[key] + pg_score)

    def rank_results(self):
        if self.cached_results is not None:
            self.cached_results = {k: v for k, v in sorted(self.cached_results.items(), key=lambda item: item[1], reverse=True)}

        if self.cached_results_expanded is not None:
            self.cached_results_expanded = {k: v for k, v in sorted(self.cached_results_expanded.items(), key=lambda item: item[1], reverse=True)}
