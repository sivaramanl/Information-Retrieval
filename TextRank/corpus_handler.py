# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 18:10:04 2020

@author: Sivaraman Lakshmipathy
"""

import os

from pagerank import *

class corpus_handler: #class to process the documents in the corpus
    def __init__(self, corpus_directory, reference_directory, window_size, mrr_obj):
        self.corpus_directory = corpus_directory
        self.reference_directory = reference_directory
        self.window_size = window_size
        self.process_documents(mrr_obj)

    def file_exists(self, file_path):
        if not os.path.exists(file_path):
            return False
        return True

    def process_documents(self, mrr_obj):
        total_file_count = 0
        documents_list = os.listdir(self.corpus_directory)

        for corpus_document in documents_list:
            if corpus_document.startswith("."):
                continue
            corpus_document_fullpath = self.corpus_directory + os.path.sep + corpus_document
            reference_document_fullpath = self.reference_directory + os.path.sep + corpus_document
            if self.file_exists(corpus_document_fullpath) and self.file_exists(reference_document_fullpath):
                total_file_count += 1
                pagerank(corpus_document_fullpath, reference_document_fullpath, self.window_size, mrr_obj)

        mrr_obj.calculate_mrr(total_file_count)
