# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:01:19 2020

@author: Sivaraman Lakshmipathy
"""

import gensim
from text_processor import *
from logger_handler import *
from persistence_handler import *

#Class to perform topic modelling using Latent Dirichlet Allocation technique
class lda:
    collectionFiles_dir = crawl_data_persistence_handler.data_dir
    id2word_save_file = os.path.dirname(os.getcwd()) + os.path.sep + "data" + os.path.sep + "lda_id2word.gensim"
    lda_model_save_file = os.path.dirname(os.getcwd()) + os.path.sep + "data" + os.path.sep + "lda_model.gensim"

    def __init__(self):
        self.id2word = None #id to word mapping
        self.lda_model = None

    def run(self):
        try:
            dataset = []
            collectionFiles = []
            if os.path.exists(self.collectionFiles_dir):
                collectionFiles = os.listdir(self.collectionFiles_dir)
            for cur_file in collectionFiles:
                cur_json = crawl_data_persistence_handler().read(cur_file)
                final_text = cur_json["content"].strip()
                #Filter out non-ASCII text
                final_text = (final_text.encode('ascii', 'ignore')).decode("utf-8")
                dataset.append(textProcessor().custom_tokenizer(final_text))
            if dataset is not None:
                custom_logger().log_message("Building the LDA model.", logger_handler.log_level_INFO)
                self.id2word = gensim.corpora.Dictionary(dataset)
                data_bow = [self.id2word.doc2bow(doc) for doc in dataset]
                try:
                    self.lda_model = gensim.models.LdaModel(data_bow, num_topics=20, id2word=self.id2word, passes=20)
                except Exception:
                    self.id2word = None
                    self.lda_model = None
                    custom_logger().log_message("Exception while training LDA model: " + str(e), logger_handler.log_level_CRITICAL)
            self.save_model()
        except Exception as e:
            custom_logger().log_message("Exception while generating LDA model: " + str(e), logger_handler.log_level_CRITICAL)
            self.id2word = None
            self.lda_model = None

    def save_model(self):
        try:
            self.id2word.save(self.id2word_save_file)
            self.lda_model.save(self.lda_model_save_file)
        except Exception as e:
            custom_logger().log_message("Exception while saving LDA model:" + str(e), logger_handler.log_level_CRITICAL)

    def load_model(self):
        try:
            self.id2word = gensim.corpora.Dictionary.load(self.id2word_save_file)
            self.lda_model = gensim.models.LdaModel.load(self.lda_model_save_file)
        except Exception as e:
            custom_logger().log_message("Exception while loading LDA model:" + str(e), logger_handler.log_level_CRITICAL)
            self.id2word = None
            self.lda_model = None

    def get_related_words(self, query, no_of_terms=5):
        if self.lda_model is None:
            custom_logger().log_message("LDA model not available.", logger_handler.log_level_WARNING)
            return []

        try:
            query_tokens = textProcessor().custom_tokenizer(query)
            query_bow = self.id2word.doc2bow(query_tokens)
            related_topic = sorted(self.lda_model.get_document_topics(query_bow), key=lambda item_new: item_new[1], reverse=True)[0][0]
            related_words = [item[0] for item in self.lda_model.show_topic(related_topic, topn=no_of_terms)]
            return related_words
        except Exception as e:
            custom_logger().log_message("Exception while fetching related words:" + str(e), logger_handler.log_level_ERROR)
            return []
