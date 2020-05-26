Aim: Implement TextRank algorithm to rank documents, and evaulate the ranking using gold standard measures.
<hr>
Dependency: Python 3.7.1
<br>
Package dependencies:
<ol>
 <li>os: to perform file operations</li>
 <li>sys: to read input arguments</li>
 <li>nltk: to perform text processing operations</li>
</ol>
<br>

<b>Executing the source code - Input arguments:</b>
<ul>
 <li>The source code expects three input arguments:
  <ul>
   <li>the directory containing the abstract documents</li>
   <li>the directory containing the gold standard documents</li>
   <li>window size</li>
  </ul>
 </li>
 <li>The source code can be executed as follows:
  <br>
  >> python textrank.py <full_path_of_abstract_documents_directory> <full_path_of_gold_standard_documents_directory> <window_size>
 </li>
 <li>If incorrect/insufficient input arguments are provided, the source code will use the default values provided during the implementation, which are as follows:
  <ul>
   <li>Abstract documents directory: .\www\abstracts</li>
   <li>Gold standard documents directory: .\www\gold</li>
   <li>Window size: 2</li>
  </ul>
 </li>
</ul>
<br>
<b>Execution outputs:</b>
<ul>
 <li>The input abstracts are loaded into an undirected word graph and page rank algorithm is used to calculate the node weights. The final scores for phrases are ranked and evaluated using Mean Reciprocal Rank (MRR) against the gold standard files.</li>
 <li>The MRR scores for top K predicted keyphrases (K ranges from 1 to 10) are provided as the output.</li>
</ul>
<br>
<b>Functionalities:</b>
The source code is split into five different components, each with its own corresponding python file.
<ol>
 <li>textProcessor.py: contains the class that encapsulates the text processing operations.</li>
 <li>mrr.py: contains the class that encapsulates the Mean Reciprocal Rank (MRR) operations.</li>
 <li>pagerank.py: encapsulates the PageRank algorithm implementation.</li>
 <li>corpus_handler.py: encapsulates the processing of the documents in the corpus.</li>
 <li>textrank.py: processes the input parameters and invokes the other modules.</li>
</ol>

The various components are discussed in detail below:
<ol>
 <li>textProcessor.py: contains the textProcessor class
  <ol>
   <li>is_stop_word(): Returns a boolean to indicate if the parameter is a stop word. Utilizes the list of stop words available in the NLTK package.
   </li>
   <li>get_stem(): Returns the stem of the target word using PorterStemmer.
   </li>
   <li>tokenize_str(): Returns the tokenized list of the target sentence. The tokenization is based on white space character.
   </li>
  </ol>
 </li>
 <li>mrr.py: contains the mrr class
  <ol>
   <li>calculate_rr(): Takes the list of phrases along with their scores and the gold standard. Calculates the MRR @ K, where K ranges from 1 to 10. If there are no matches, MRR @ K is 0 for the document.
   </li>
   <li>calculate_mrr(): Calculates the final MRR by taking the mean of the accumulates MRR @ K values.
   </li>
   <li>pretty_print(): Prints the MRR @ K values.
   </li>
  </ol>
 </li>
 <li>pagerank.py: contains the pagerank class.
  <ol>
   <li>The objective of this class is to encapsulate the following actions:
    <ol>
     <li>Generate the word graph from the abstract document.</li>
     <li>Run the page rank algorithm on the graph to calculate the weighted score for each node in the graph.</li>
     <li>Invoke the MRR calculation.</li>
     <li>The default values utilized for the different parameters are listed below.
      <ol>
       <li>Valid POS list - NN, NNS, NNP, NNPS, JJ</li>
       <li>Alpha (utilized in score updates) - 0.85</li>
       <li>Maximum number of iterations for Pagerank - 10</li>
       <li>Maximum n-gram size - 3</li>
      </ol>
     </li>
    </ol>
   </li>
   <li>global_handler(): Read the contents of the abstract and the gold standard, invoke the PageRank component.</li>
   <li>build_reference_set(): Load the gold standard file, stem the words and construct the final reference set.</li>
   <li>validate(): Validates the given token and its POS tag. It checks if the word is a stop word or not. It also validates the POS tag. Any word in the document that fails the validation is not considered to be a candidate node.</li>
   <li>generate_word_graph():
    <ol>
     <li>The document is processed and loaded into an undirected graph.</li>
     <li>The graph is represented using the adjacency list representation. Each node is linked to all its neighbors along with the weights.</li>
     <li>A word is considered to be a candidate node if it is not a stop word and its POS tag is one of the valid pre-configured values.</li>
     <li>An edge is added between two nodes if they occur together in the document in the same window. The entire document is considered to be a single sequence to find the edges.</li>
    </ol>
   </li>
   <li>create_node_weights(): A helper function to create the node weights in the graph.</li>
   <li>update_node_weights(): A helper function to update the node weights in the graph.</li>
   <li>initialize_params(): Initialize the parameters for the PageRank component.</li>
   <li>run_pagerank(): Calculates the score for the nodes in the graph iteratively for a predefined number of iterations.</li>
   <li>get_ngram_scores():
    <ol>
     <li>Generate the n-grams from the original text and calculates the score for the phrases using the individual scores generated in the PageRank component.</li>
     <li>The bigrams and trigrams are generated in this implementation.</li>
     <li>The entire document is considered to be a single sequence to generate the n-grams.</li>
    </ol>
   </li>
   <li>rank_scores(): Rank the scores in ascending/descending order.</li>
  </ol>
 </li>
 <li>corpus_handler.py: contains the corpus_handler class
  <ol>
   <li>The objective of this component is to process each document in the corpus and invoke the PageRank component on valid documents.</li>
   <li>file_exists(): A helper function to check if the file exists or not.</li>
   <li>process_documents(): For each abstract document, it verifies if the gold standard document is available, and invokes the PageRank component. Finally, it invokes the MRR component to calculate the final MRR @ K values.</li>
  </ol>
 </li>
</ol>
<br> 
<b>Results:</b>
<br>1.	Window size = 2
<br>
<br>Processing the documents with window size 2 ...
<br>MRR for top 01 documents : 0.055639097744360905
<br>MRR for top 02 documents : 0.08007518796992481
<br>MRR for top 03 documents : 0.10112781954887208
<br>MRR for top 04 documents : 0.12086466165413534
<br>MRR for top 05 documents : 0.1360526315789473
<br>MRR for top 06 documents : 0.14682957393483684
<br>MRR for top 07 documents : 0.15273720014321482
<br>MRR for top 08 documents : 0.15696652345148548
<br>MRR for top 09 documents : 0.16072592194772614
<br>MRR for top 10 documents : 0.16433494450411704
<br><br>
2.	Window size = 6
<br>
<br>Processing the documents with window size 6 ...
<br>MRR for top 01 documents : 0.06842105263157895
<br>MRR for top 02 documents : 0.10488721804511278
<br>MRR for top 03 documents : 0.1339598997493735
<br>MRR for top 04 documents : 0.15313283208020068
<br>MRR for top 05 documents : 0.16636591478696724
<br>MRR for top 06 documents : 0.17626566416040057
<br>MRR for top 07 documents : 0.1827103472968129
<br>MRR for top 08 documents : 0.18665771571786552
<br>MRR for top 09 documents : 0.19100190953574364
<br>MRR for top 10 documents : 0.19415980427258564
