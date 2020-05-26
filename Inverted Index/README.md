<b>Inverted index implementation</b>
<hr>
Aim: Process a data corpus, generate the inverted index and process input queries to identify relevant documents. The final results are evaluated against human verified results.
<hr>
Dependency: Python 3.7.1
<br><br>
Package dependencies:
<ol>
	<li>os: to perform file operations</li>
	<li>sys: to read input arguments</li>
	<li>string: to handle punctuations in the text</li>
	<li>zipfile: to extract contents from the zip file</li>
	<li>nltk: to perform text processing operations</li>
	<li>bs4: to parse the corpora</li>
	<li>math: to perform math operations</li>
</ol>

<b>Executing the source code - Input arguments:</b>
<ul>
	<li>The source code expects a minimum of two arguments - the first one for the query file and the second one for the relevance file.
		<br>
		>> python main.py full_path_of_query_file full_path_of_relevance_file
	</li>
	<li>In this scenario, the source code looks for a directory named ‘cranfieldDocs’ and processes all documents in the directory. If the directory is unavailable, it tries to extract contents from ‘cranfield.tar.gz’ (intending to result in a directory named ‘cranfieldDocs’). If both operations fail, the source code exits.</li>
	<li>If the end-user seeks to utilize a different directory, the full path can be provided as the third argument while running the code.
		<br>
		>> python main.py full_path_of_query_file full_path_of_relevance_file full_path_of_directory
	</li>
	<li>If the end-user seeks to provide a zip file name (to be extracted), it can be provided as the thid argument while running the code along with the directory name to be processed as the fourth argument.
		<br>
		>> python main.py full_path_of_query_file full_path_of_relevance_file full_path_of_zip_file full_path_of_directory
		<br>
		Note: The files will be extracted to the current directory of the source code.
	</li>
	<li>If no/insufficient arguments are provided, the source code will use default values for the file names (provided during the implementation).</li>
</ul>
 
<b>Execution outputs:</b>
<ul>
	<li>The precision and recall for the list of queries in the query file is evaluated at ranks 10,50,100 and 500 and generated as the output of the implementation.</li>
	<li>The average precision and recall for each rank are also provided.</li>
</ul>

<b>Functionalities:</b>
<br>
The source code comprises of three classes, with the hierarchy as follows.
<ol>
	<li>textProcessor: holds the methods to process text.</li>
	<li>corpusHandler(textProcessor): extends textProcessor class and holds methods to process the corpora and generate the inverted index data structure.</li>
	<li>queryHandler(textProcessor): extends textProcessor class and performs the tasks of calculation of cosine similarity, ranking, and metrics calculation.</li>
</ol>

The various functionalities are discussed below:
<ol>
	<li>textProcessor class:
		<ul>
			<li>Punctuation and numbers removal: remove_punctuation_numbers()
				<br>
				All punctuations and numbers are removed from the text.
			</li>
			<li>Tokenization: tokenize_str()
				<br>
				To tokenize the string to perform further operations.
			</li>
			<li>Stopwords removal: eliminate_stopwords()
			</li>
			<li>Stemming: perform_stemming()
			</li>
			<li>Filter words with minimum length:filter_minimumum_length()
				<br>
				Eliminate words that do not meet the minimum length criteria.
			</li>
			<li>Extract integer value: get_int_from_str()
				<br>
				To extract integer value from strings. Used for extracting document ids from document names.
			</li>
		</ul>
	</li>
	<li>corpusHandler class:
		<ul>
			<li>Process the corpora: process_collection()
				<br>
				Processes the files in the corpora directory, extracts the title and text contents alone for each file using BeautifulSoup package, initiates the inverted index construction.
			</li>
			<li>Building the data structure:build_term_frequency()
				<br>
				Builds the inverted index data structure. The general structure of the dictionary object being constructed is as follows:
				<br>
{
<br>&nbsp;&nbsp;&nbsp;&nbsp;token1: 
<br>&nbsp;&nbsp;&nbsp;&nbsp;{
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	df: document_frequency,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	tf:
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	{
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;		doc_id_1: term_frequency_1,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;		doc_id_2: term_frequency_2
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	   }
<br>&nbsp;&nbsp;&nbsp;&nbsp;	}
<br>}
			</li>
			<li>Generating document lengths: generate_doc_length()
				<br>
				Performs a second pass over all the documents and generates the document length for each document. This value is utilized later to calculate the cosine similarity between the query and the document.
			</li>
		</ul>
	</li>
	<li>queryHandler class:
		<ul>
			<li>Get relevance details: readRelevance()
				<br>
				Read and store the relevance details for each query in order to generate the precision and recall metrics.
			</li>
			<li>Process queries: process_queries()
				<br>
				Reads the queries one by one from the queries file, initiates the cosine similarity calculation and performs ranking. It also initiates the generation of the output.
			</li>
			<li>Calculate cosine similarity: generate_cosine_similarity()
				<br>
				Generates cosine similarity by incrementally calculating the product of the weights for each term in the query with the relevant documents.
			</li>
			<li>Generate metrics: calculate_metrics()
				<br>
				Calculates the precision and recall for the given cosine similarity of each query at ranks 10, 50, 100 and 500. The ranks are hardcoded.
			</li>
			<li>Output generation: pretty_print()
				<br>
				Generate the output in the required format. It is directed to the default output stream.
			</li>
		</ul>
	</li>
</ol>

<u>Sample results:</u>
<br>
Evaluating your queries...
<br>
Top 10 documents in rank list
<br>
Query:  1 	Pr:  0.0 	Re:  0.0
<br>
Query:  2 	Pr:  0.2 	Re:  0.13333333333333333
<br>
Query:  3 	Pr:  0.2 	Re:  0.13333333333333333
<br>
Query:  4 	Pr:  0.1 	Re:  0.05555555555555555
<br>
Query:  5 	Pr:  0.1 	Re:  0.05263157894736842
<br>
Query:  6 	Pr:  0.4 	Re:  0.2222222222222222
<br>
Query:  7 	Pr:  0.6 	Re:  0.6666666666666666
<br>
Query:  8 	Pr:  0.2 	Re:  0.5
<br>
Query:  9 	Pr:  0.0 	Re:  0.0
<br>
Query:  10 	Pr:  0.2 	Re:  0.08333333333333333
<br>
<br>

Avg precision: 0.2
<br>
Avg recall: 0.18470760233918126
<br>
<br>

Top 50 documents in rank list
<br>
Query:  1 	Pr:  0.0 	Re:  0.0
<br>
Query:  2 	Pr:  0.12 	Re:  0.4
<br>
Query:  3 	Pr:  0.12 	Re:  0.4
<br>
Query:  4 	Pr:  0.04 	Re:  0.1111111111111111
<br>
Query:  5 	Pr:  0.14 	Re:  0.3684210526315789
<br>
Query:  6 	Pr:  0.14 	Re:  0.3888888888888889
<br>
Query:  7 	Pr:  0.16 	Re:  0.8888888888888888
<br>
Query:  8 	Pr:  0.06 	Re:  0.75
<br>
Query:  9 	Pr:  0.12 	Re:  0.75
<br>
Query:  10 	Pr:  0.08 	Re:  0.16666666666666666
<br>
<br>

Avg precision: 0.098
<br>
Avg recall: 0.4223976608187135
<br>
<br>

Top 100 documents in rank list
<br>
Query:  1 	Pr:  0.0 	Re:  0.0
<br>
Query:  2 	Pr:  0.09 	Re:  0.6
<br>
Query:  3 	Pr:  0.09 	Re:  0.6
<br>
Query:  4 	Pr:  0.06 	Re:  0.3333333333333333
<br>
Query:  5 	Pr:  0.12 	Re:  0.631578947368421
<br>
Query:  6 	Pr:  0.09 	Re:  0.5
<br>
Query:  7 	Pr:  0.09 	Re:  1.0
<br>
Query:  8 	Pr:  0.03 	Re:  0.75
<br>
Query:  9 	Pr:  0.06 	Re:  0.75
<br>
Query:  10 	Pr:  0.04 	Re:  0.16666666666666666
<br>
<br>


Avg precision: 0.06699999999999999
<br>
Avg recall: 0.5331578947368422
<br>
<br>

Top 500 documents in rank list
<br>
Query:  1 	Pr:  0.002 	Re:  1.0
<br>
Query:  2 	Pr:  0.03 	Re:  1.0
<br>
Query:  3 	Pr:  0.03 	Re:  1.0
<br>
Query:  4 	Pr:  0.032 	Re:  0.8888888888888888
<br>
Query:  5 	Pr:  0.038 	Re:  1.0
<br>
Query:  6 	Pr:  0.034 	Re:  0.9444444444444444
<br>
Query:  7 	Pr:  0.018 	Re:  1.0
<br>
Query:  8 	Pr:  0.008 	Re:  1.0
<br>
Query:  9 	Pr:  0.016 	Re:  1.0
<br>
Query:  10 	Pr:  0.026 	Re:  0.5416666666666666
<br>
<br>

Avg precision: 0.0234
<br>
Avg recall: 0.9375
