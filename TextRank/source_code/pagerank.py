"""
Created on Tue Apr 14 18:10:04 2020

@author: Sivaraman Lakshmipathy
"""

from textProcessor import *
from mrr import *

class pagerank: #class to build word graph and perform page rank on individual documents
    pos_list = ["NN", "NNS", "NNP", "NNPS", "JJ"] #valid pos tags
    alpha = 0.85
    beta = 0
    no_of_iterations = 10
    max_ngram = 3
    tObj = textProcessor()

    def __init__(self, file_path, reference_file_path, window_size, mrr_obj):
        self.file_path = file_path
        self.reference_file_path = reference_file_path
        self.window_size = window_size

        self.adj_list = {}
        self.adj_list_weight_sum = {}
        self.doc_tokens = []
        self.nodes_size = 0
        self.pi = 0
        self.scores = {}
        self.modified_text = []
        self.gold_standard = {}

        self.global_handler(mrr_obj)

    def global_handler(self, mrr_obj):
        with open(self.file_path) as f:
            cur_doc = f.read()
            self.doc_tokens = self.tObj.tokenize_str(cur_doc)
        self.build_reference_set() #gold standard
        self.generate_word_graph()
        self.run_pagerank()
        mrr_obj.calculate_rr(self.scores, self.gold_standard)

    def build_reference_set(self): #to load the gold standard
        with open(self.reference_file_path) as f:
            content = f.readlines()
        stem_content = []
        for entry in content:
            process_entry = self.tObj.tokenize_str(entry)
            cur_str = ""
            for ele in process_entry:
                if not self.tObj.is_stop_word(ele):
                    cur_str += " " + self.tObj.get_stem(ele)
                else:
                    cur_str += " " + ele
            cur_str = cur_str.strip()
            stem_content.append(cur_str)
        self.gold_standard = set(stem_content)

    def run_pagerank(self): #run the pagerank algorithm on the word graph
        if self.initialize_params():
            for i in range(self.no_of_iterations):
                new_score = {}
                for node in self.scores:
                    neighbours = self.adj_list[node]
                    node_sum = 0
                    for neighbour in neighbours:
                        node_sum += neighbours[neighbour] / self.adj_list_weight_sum[neighbour] * self.scores[neighbour]
                    new_score[node] = (self.alpha * node_sum) + self.beta
                self.scores = new_score

            self.scores = self.rank_scores(self.scores)
            self.get_ngram_scores()

    def get_ngram_scores(self): #generate ngrams and calculate corresponding scores
        for i in range(2, self.max_ngram+1):
            for j in range(len(self.doc_tokens) - i):
                cur_ngram, cur_ngram_pos, toProcess = self.validate(self.doc_tokens[j])
                if toProcess:
                    ngram = "" + cur_ngram
                    ngram_score = self.scores[cur_ngram]
                    for k in range(1, i):
                        temp_ngram, temp_ngram_pos, toProcessNested = self.validate(self.doc_tokens[j + k])
                        if toProcessNested:
                            ngram += " " + temp_ngram
                            ngram_score += self.scores[temp_ngram]
                        else:
                            ngram = None
                            break
                    if ngram is not None:
                        self.scores[ngram] = ngram_score

        self.scores = self.rank_scores(self.scores)

    def rank_scores(self, scores, reverse=True):
        return {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=reverse)}

    def initialize_params(self):
        self.nodes_size = len(self.adj_list.keys())

        if self.nodes_size < 1:
            return False

        self.pi = 1/self.nodes_size

        self.beta = ((1 - self.alpha) * self.pi)

        for key in self.adj_list.keys():
            self.scores[key] = 1/self.nodes_size

        return True

    def generate_word_graph(self): #generate the word graph for the current document with the configured window size
        tokens_len = len(self.doc_tokens)
        indx = 0
        for token in self.doc_tokens:
            cur_token, cur_pos, toProcess = self.validate(token)
            if toProcess:
                self.modified_text += [cur_token]
                self.create_node_weights(cur_token)
                window = 1
                while window < self.window_size and indx + window < tokens_len:
                    cur_neighbour = self.doc_tokens[indx + window]
                    window += 1
                    cur_neighbour, cur_neighbour_pos, toProcessNested = self.validate(cur_neighbour)
                    if toProcessNested:
                        self.update_node_weights(cur_token, cur_neighbour)
                        self.update_node_weights(cur_neighbour, cur_token)
            indx += 1

    def create_node_weights(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = {}
            self.adj_list_weight_sum[node] = 0

    def update_node_weights(self, node_a, node_b):
        self.create_node_weights(node_a)
        neighbour_a = self.adj_list[node_a]
        if node_b not in neighbour_a:
            neighbour_a[node_b] = 1
        else:
            neighbour_a[node_b] += 1
        self.adj_list_weight_sum[node_a] += 1

    def validate(self, token):
        entries = token.split("_")
        if len(entries) != 2:
            return None, None, False
        cur_token = entries[0]
        cur_pos = entries[1]
        if cur_pos not in self.pos_list or self.tObj.is_stop_word(cur_token):
            return None, None, False
        return self.tObj.get_stem(cur_token), cur_pos, True
