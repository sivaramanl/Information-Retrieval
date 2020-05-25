# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:01:19 2020

@author: Sivaraman Lakshmipathy
"""

import sys
from lda import *
from tkinter import *
from indexer import *
from crawler import *
from pagerank import *
from query_handler import *
from logger_handler import *

#Class to load all the required models
class startup:

    def run(self):
        print("Initializing engine components")
        return self.load_components()

    def load_components(self, count=0):
        if count >= 2: #If the loader fails for 2 consecutive times, exit the engine
            custom_logger().log_message("Unable to load the engine. Exiting.", logger_handler.log_level_CRITICAL)
            print("Unable to load the engine. Exiting.")
            sys.exit(0)
        graph_obj = pagerank().unpickle_graph()
        indexer_obj = indexer().unpickle_indexer()
        if graph_obj is not None and indexer_obj is not None:
            lda_obj = lda()
            lda_obj.load_model()
            return graph_obj, indexer_obj, lda_obj

        if count > 0:
            custom_logger().log_message("Unexpected error while trying to launch engine. Trying again.", logger_handler.log_level_ERROR)
            print("Unexpected error while trying to launch engine. Trying again.")

        #Prompt the user to reconstruct the models again
        val = input("Processed information not found. Do you want to crawl again? (y/n) ")
        val = val.lower()
        if val == 'y' or val == 'yes':
            try:
                print("Launching web crawler. This operation will take a while to complete.")
                crawler()
                print("Web crawler operations completed! Launching components.")
                return self.load_components(count + 1)
            except Exception as e:
                custom_logger().log_message("Unexpected error while crawling the web. Exiting.\n" + str(e),
                                            logger_handler.log_level_CRITICAL)
                print("Unexpected error while crawling the web. Exiting.")
                sys.exit(0)
        else:
            custom_logger().log_message("Unable to load the search engine without the required components. Exiting.", logger_handler.log_level_CRITICAL)
            print("Unable to load the search engine without the required components. Exiting.")
            sys.exit(0)

class interface:
    similarity_measures = query_handler.similarity_measures

    def __init__(self):
        self.gui_option = 1
        self.search_query = None
        self.similarity_measure = 3
        self.graph_obj = None
        self.indexer_obj = None
        self.query_handler = None
        self.lda_obj = None

        #GUI
        self.window = None
        self.new_search_button = None
        self.search_button = None
        self.prev_button = None
        self.next_button = None
        self.query_input = None
        self.query_input_label = None
        self.radio_option = None
        self.result_text = None
        self.result_text2 = None
        self.exit_button = None
        self.result_val = None
        self.result_val2 = None

    #GUI methods
    def gui_load(self):
        self.window = Tk()
        self.window.title("Search Engine")
        input_frame = Frame(self.window)
        radio_frame = Frame(self.window)
        results_frame = Frame(self.window)
        results_frame2 = Frame(self.window)
        bottom_frame = Frame(self.window)
        input_frame.pack(side="top", fill="both", expand=True)
        radio_frame.pack(side="top", fill="both", expand=True)
        results_frame.pack(side="top", fill="both", expand=True)
        results_frame2.pack(side="top", fill="both", expand=True)
        bottom_frame.pack(side="bottom", fill="both", expand=True)

        self.query_input_label = Label(input_frame, text="Enter your search query:")
        self.query_input_label.pack(side=TOP)
        self.query_input = Entry(input_frame, width=30)
        self.query_input.pack(side=TOP)

        Label(radio_frame, text="Select similarity measure:").pack(side=LEFT)
        self.radio_option = IntVar()
        for i in range(len(self.similarity_measures)):
            radio_var = Radiobutton(radio_frame, text=self.similarity_measures[i], variable=self.radio_option, value=i+1)
            radio_var.pack(side=LEFT)
        self.radio_option.set(self.similarity_measure)

        self.result_val = StringVar()
        self.result_text = Label(results_frame, textvariable=self.result_val)
        self.result_text.pack(side=TOP)
        self.result_val.set("")
        self.result_val2 = StringVar()
        self.result_text = Label(results_frame2, textvariable=self.result_val2)
        self.result_text.pack(side=TOP)
        self.result_val2.set("")

        self.new_search_button = Button(bottom_frame, text="New Search", state=DISABLED, command=self.initiate_new_search)
        self.prev_button = Button(bottom_frame, text="<< Prev", state=DISABLED, command=self.fetch_previous)
        self.search_button = Button(bottom_frame, text="Search", command=self.submit_query)
        self.next_button = Button(bottom_frame, text="Next >>", state=DISABLED, command=self.fetch_next)
        self.exit_button = Button(bottom_frame, text="Exit", command=self.exit_interface)
        self.new_search_button.pack(side=LEFT)
        Label(bottom_frame, text="                      ").pack(side=LEFT)
        self.prev_button.pack(side=LEFT)
        Label(bottom_frame, text="                      ").pack(side=LEFT)
        self.search_button.pack(side=LEFT)
        Label(bottom_frame, text="                      ").pack(side=LEFT)
        self.next_button.pack(side=LEFT)
        Label(bottom_frame, text="                      ").pack(side=LEFT)
        self.exit_button.pack(side=RIGHT)
        self.window.mainloop()

    def initiate_new_search(self):
        self.new_search_button['state'] = DISABLED
        self.next_button['state'] = DISABLED
        self.prev_button['state'] = DISABLED
        self.query_input['state'] = NORMAL
        self.search_button['state'] = ACTIVE

    def exit_interface(self):
        sys.exit(0)

    def fetch_next(self):
        results, results_expanded, canNext, canPrev = self.query_handler.get_next_resultset()
        self.display_results_gui(results, results_expanded, canNext, canPrev)

    def fetch_previous(self):
        results, results_expanded, canNext, canPrev = self.query_handler.get_previous_resultset()
        self.display_results_gui(results, results_expanded, canNext, canPrev)

    def submit_query(self):
        cur_query = self.query_input.get().strip()
        if cur_query is not None and not cur_query == "":
            results, results_expanded, canNext, canPrev = self.query_handler.getResults(cur_query, self.similarity_measure)
            self.display_results_gui(results, results_expanded, canNext, canPrev)
        else:
            self.query_input.delete(1, END)

    def display_results_gui(self, results, results_expanded, canNext, canPrev):
        result_str = "Search Results:\n"
        if len(results) == 0:
            result_str += "No results."
        else:
            for url in results:
                result_str += url
                result_str += "\n"
        self.result_val.set(result_str)
        result_str_expanded = "Search Results (with expanded query):\n"
        if len(results_expanded) == 0:
            result_str_expanded += "No results."
        else:
            for url in results_expanded:
                result_str_expanded += url
                result_str_expanded += "\n"
        self.result_val2.set(result_str_expanded)
        self.radio_option.set(self.similarity_measure)
        self.query_input['state'] = DISABLED
        self.search_button['state'] = DISABLED
        self.new_search_button['state'] = ACTIVE
        if canNext:
            self.next_button['state'] = ACTIVE
        else:
            self.next_button['state'] = DISABLED
        if canPrev:
            self.prev_button['state'] = ACTIVE
        else:
            self.prev_button['state'] = DISABLED

    #Command line interface methods
    def interface_initializer(self):
        print("Welcome to the search engine.")
        print("1. Use the command line")
        print("2. Launch the GUI")
        print("3. Exit")
        try:
            choice = int(input("Enter your choice: "))
        except Exception:
            choice = 0
        if choice == 3:
            sys.exit(0)
        if choice == 1 or choice == 2:
            self.gui_option = choice
            return
        print("Unsupported option!\n")
        return self.interface_initializer()

    def get_query(self):
        search_query = input("\nPlease enter the search query: ")
        self.confirm_similarity_measure()
        return search_query

    def confirm_similarity_measure(self):
        print("The configured similarity measure is", self.similarity_measures[self.similarity_measure-1])
        choice = input("Do you want to reconfigure? (y/n) ")
        choice = choice.lower()
        if choice == 'y' or choice == 'yes':
            self.update_similarity_measure()

    def update_similarity_measure(self):
        for i in range(1, len(self.similarity_measures)+1):
            print(i, self.similarity_measures[i-1])
        try:
            choice = int(input("Enter your choice: "))
        except Exception:
            choice = 0
        if choice in range(1, len(self.similarity_measures)+1):
            self.similarity_measure = choice
            return
        print("Unsupported option!\n")
        return self.update_similarity_measure()

    def display_results(self, results, results_expanded, canNext):
        print("\nSearch Results:")
        if len(results) == 0:
            print("No results.")

        for url in results:
            print(url)

        print("\nSearch Results (with expanded query):")
        if len(results_expanded) == 0:
            print("No results.")

        for url in results_expanded:
            print(url)

        if canNext:
            choice = input("Do you want to fetch more search results? (y/n) ")
            choice = choice.lower()
            if choice == 'y' or choice == 'yes':
                return True
        return False

    def confirm_new_search(self):
        choice = input("\nDo you want to start a new search? (y/n) ")
        choice = choice.lower()
        if choice == 'y' or choice == 'yes':
            return True
        return False

    def run(self):
        self.graph_obj, self.indexer_obj, self.lda_obj = startup().run()
        self.query_handler = query_handler(self.indexer_obj, self.graph_obj, self.lda_obj)
        custom_logger().log_message("Launching the search engine.", logger_handler.log_level_INFO)
        self.interface_initializer()

        if self.gui_option == 1:
            new_search = True
            while True:
                if new_search:
                    cur_query = self.get_query()
                    results, results_expanded, canNext, _ = self.query_handler.getResults(cur_query, self.similarity_measure)
                    fetch_more = self.display_results(results, results_expanded, canNext)
                else:
                    results, results_expanded, canNext, _ = self.query_handler.get_next_resultset()
                    fetch_more = self.display_results(results, results_expanded, canNext)
                if fetch_more:
                    new_search = False
                    continue
                new_search = True
                if not self.confirm_new_search():
                    break
        elif self.gui_option == 2:
            self.gui_load()

def main():
    interface_obj = interface()
    interface_obj.run()

if __name__ == "__main__":
    main()
