Source code name: slaksh5_hw4.py
Programming language: Python 3.7.1

Package dependencies:
1.	os: to perform file operations
2.	sys: to read input arguments
3.	nltk: to perform text processing operations

Executing the source code - Input arguments:
●	The source code expects three input arguments:
○	the directory containing the abstract documents
○	the directory containing the gold standard documents
○	window size
●	The source code can be executed as follows:
>> python slaksh5_hw4.py <full_path_of_abstract_documents_directory> <full_path_of_gold_standard_documents_directory> <window_size>
●	If incorrect/insufficient input arguments are provided, the source code will use the default values provided during the implementation, which are as follows:
○	Abstract documents directory: .\www\abstracts
○	Gold standard documents directory: .\www\gold
○	Window size: 2

Execution outputs:
●	The input abstracts are loaded into an undirected word graph and page rank algorithm is used to calculate the node weights. The final scores for phrases are ranked and evaluated using Mean Reciprocal Rank (MRR) against the gold standard files.
●	The MRR scores for top K predicted keyphrases (K ranges from 1 to 10) are provided as the output.

Functionalities:
The source code is split into five different components, each with its own corresponding python file.
1.	textProcessor.py: contains the class that encapsulates the text processing operations.
2.	mrr.py: contains the class that encapsulates the Mean Reciprocal Rank (MRR) operations.
3.	pagerank.py: encapsulates the PageRank algorithm implementation.
4.	corpus_handler.py: encapsulates the processing of the documents in the corpus.
5.	slaksh5_hw4.py: processes the input parameters and invokes the other modules.

The various components are discussed in detail below:

1.	textProcessor.py: contains the textProcessor class
a.	is_stop_word():
Returns a boolean to indicate if the parameter is a stop word. Utilizes the list of stop words available in the NLTK package.
b.	get_stem():
Returns the stem of the target word using PorterStemmer.
c.	tokenize_str():
Returns the tokenized list of the target sentence. The tokenization is based on white space character.
2.	mrr.py: contains the mrr class
a.	calculate_rr():
Takes the list of phrases along with their scores and the gold standard. Calculates the MRR @ K, where K ranges from 1 to 10. If there are no matches, MRR @ K is 0 for the document.
b.	calculate_mrr():
Calculates the final MRR by taking the mean of the accumulates MRR @ K values.
c.	pretty_print():
Prints the MRR @ K values.
3.	pagerank.py: contains the pagerank class. 
a.	The objective of this class is to encapsulate the following actions:
i.	Generate the word graph from the abstract document.
ii.	Run the page rank algorithm on the graph to calculate the weighted score for each node in the graph.
iii.	Invoke the MRR calculation.
iv.	The default values utilized for the different parameters are listed below.
1.	Valid POS list - NN, NNS, NNP, NNPS, JJ
2.	Alpha (utilized in score updates) - 0.85
3.	Maximum number of iterations for Pagerank - 10
4.	Maximum n-gram size - 3
b.	global_handler():
Read the contents of the abstract and the gold standard, invoke the PageRank component.
c.	build_reference_set():
Load the gold standard file, stem the words and construct the final reference set.
d.	validate():
Validates the given token and its POS tag. It checks if the word is a stop word or not. It also validates the POS tag. Any word in the document that fails the validation is not considered to be a candidate node.
e.	generate_word_graph():
i.	The document is processed and loaded into an undirected graph.
ii.	The graph is represented using the adjacency list representation. Each node is linked to all its neighbors along with the weights.
iii.	A word is considered to be a candidate node if it is not a stop word and its POS tag is one of the valid pre-configured values.
iv.	An edge is added between two nodes if they occur together in the document in the same window. The entire document is considered to be a single sequence to find the edges.
f.	create_node_weights():
A helper function to create the node weights in the graph.
g.	update_node_weights():
A helper function to update the node weights in the graph.
h.	initialize_params():
Initialize the parameters for the PageRank component.
i.	run_pagerank():
Calculates the score for the nodes in the graph iteratively for a predefined number of iterations.
 
j.	get_ngram_scores():
i.	Generate the n-grams from the original text and calculates the score for the phrases using the individual scores generated in the PageRank component. 
ii.	The bigrams and trigrams are generated in this implementation.
iii.	The entire document is considered to be a single sequence to generate the n-grams.
k.	rank_scores():
Rank the scores in ascending/descending order.
4.	corpus_handler.py: contains the corpus_handler class
a.	The objective of this component is to process each document in the corpus and invoke the PageRank component on valid documents.
b.	file_exists():
A helper function to check if the file exists or not.
c.	process_documents():
For each abstract document, it verifies if the gold standard document is available, and invokes the PageRank component. Finally, it invokes the MRR component to calculate the final MRR @ K values.
 
Results:
1.	Window size = 2

Processing the documents with window size 2 ...
MRR for top 01 documents : 0.055639097744360905
MRR for top 02 documents : 0.08007518796992481
MRR for top 03 documents : 0.10112781954887208
MRR for top 04 documents : 0.12086466165413534
MRR for top 05 documents : 0.1360526315789473
MRR for top 06 documents : 0.14682957393483684
MRR for top 07 documents : 0.15273720014321482
MRR for top 08 documents : 0.15696652345148548
MRR for top 09 documents : 0.16072592194772614
MRR for top 10 documents : 0.16433494450411704


2.	Window size = 6

Processing the documents with window size 6 ...
MRR for top 01 documents : 0.06842105263157895
MRR for top 02 documents : 0.10488721804511278
MRR for top 03 documents : 0.1339598997493735
MRR for top 04 documents : 0.15313283208020068
MRR for top 05 documents : 0.16636591478696724
MRR for top 06 documents : 0.17626566416040057
MRR for top 07 documents : 0.1827103472968129
MRR for top 08 documents : 0.18665771571786552
MRR for top 09 documents : 0.19100190953574364
MRR for top 10 documents : 0.19415980427258564



