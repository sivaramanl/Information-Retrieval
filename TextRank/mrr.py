# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 18:10:04 2020

@author: Sivaraman Lakshmipathy
"""

class mrr: #class to calculate the Mean reciprocal rank

    def __init__(self, max_k=10):
        self.k = max_k
        self.mrr = [0] * self.k

    def calculate_rr(self, ranked_entries, gold_standard):
        for i in range(1, self.k+1):
            rank = 1
            for ngram in ranked_entries.keys():
                if ngram in gold_standard:
                    self.mrr[i-1] += 1/rank
                    break
                rank += 1
                if rank > i:
                    break
            i += 1

    def calculate_mrr(self, d):
        if d > 0:
            self.mrr = [item/d for item in self.mrr]

    def pretty_print(self):
        for i in range(self.k):
            indx = str((i+1))
            if i < 9:
                indx = "0" + str(indx)
            print("MRR for top", indx, "documents :", self.mrr[i])
