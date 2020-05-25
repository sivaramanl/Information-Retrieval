# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 18:10:04 2020

@author: Sivaraman Lakshmipathy
"""

import sys

from corpus_handler import *

def main():
    abstracts_file_directory = "." + os.path.sep + "www" + os.path.sep + "abstracts"
    gold_file_directory = "." + os.path.sep + "www" + os.path.sep + "gold"
    window_size = 2
    try:
        if len(sys.argv) >= 4:
            abstracts_file_directory = sys.argv[1]
            gold_file_directory = sys.argv[2]
            window_size = int(sys.argv[3])
        else:
            print("Insufficient input parameters. Reverting to default directories and window size.")
    except Exception as e:
        print("Unknown exception while assigning parameter values. Reverting to default directories and window size.")
        abstracts_file_directory = "." + os.path.sep + "www" + os.path.sep + "abstracts"
        gold_file_directory = "." + os.path.sep + "www" + os.path.sep + "gold"
        window_size = 2
    if not os.path.exists(abstracts_file_directory):
        print("Abstracts directory not found. Exiting.")
        return
    if not os.path.exists(gold_file_directory):
        print("Gold file directory not found. Exiting.")
        return
    if window_size == -1:
        print("Window size not specified. Exiting.")
        return

    print("Processing the documents with window size", window_size, "...")
    mrr_obj = mrr(10)
    corpus_handler(abstracts_file_directory, gold_file_directory, window_size, mrr_obj)
    mrr_obj.pretty_print()

if __name__ == "__main__":
    main()
