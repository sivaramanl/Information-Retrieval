Inverted index implementation

Programming language: Python 3.7.1

Package dependencies:
1.	os: to perform file operations
2.	sys: to read input arguments
3.	string: to handle punctuations in the text
4.	zipfile: to extract contents from the zip file
5.	nltk: to perform text processing operations
6.	bs4: to parse the corpora
7.	math: to perform math operations

Executing the source code - Input arguments:
●	The source code expects a minimum of two arguments - the first one for the query file and the second one for the relevance file.
Ex:
>> python slaksh5_hw2.py <full_path_of_query_file> <full_path_of_relevance_file>
●	In this scenario, the source code looks for a directory named ‘cranfieldDocs’ and processes all documents in the directory. If the directory is unavailable, it tries to extract contents from ‘cranfield.tar.gz’ (intending to result in a directory named ‘cranfieldDocs’). If both operations fail, the source code exits.
●	If the end-user seeks to utilize a different directory, the full path can be provided as the third argument while running the code.
Ex:
>> python slaksh5_hw2.py <full_path_of_query_file> <full_path_of_relevance_file> <full_path_of_directory>
●	If the end-user seeks to provide a zip file name (to be extracted), it can be provided as the thid argument while running the code along with the directory name to be processed as the fourth argument.
Ex:
>> python slaksh5_hw2.py <full_path_of_query_file> <full_path_of_relevance_file> <full_path_of_zip_file> <full_path_of_directory>
Note: The files will be extracted to the current directory of the source code.
●	If no/insufficient arguments are provided, the source code will use default values for the file names (provided during the implementation).
 
Execution outputs:
●	The precision and recall for the list of queries in the query file is evaluated at ranks 10,50,100 and 500 and generated as the output of the implementation.
●	The average precision and recall for each rank are also provided.

Functionalities:
The source code comprises of three classes, with the hierarchy as follows.
1.	textProcessor: holds the methods to process text.
2.	corpusHandler(textProcessor): extends textProcessor class and holds methods to process the corpora and generate the inverted index data structure.
3.	queryHandler(textProcessor): extends textProcessor class and performs the tasks of calculation of cosine similarity, ranking, and metrics calculation.

The various functionalities are discussed below:
1.	textProcessor class:
a.	Punctuation and numbers removal: remove_punctuation_numbers()
All punctuations and numbers are removed from the text.
b.	Tokenization: tokenize_str()
To tokenize the string to perform further operations.
c.	Stopwords removal: eliminate_stopwords()
d.	Stemming: perform_stemming()
e.	Filter words with minimum length:filter_minimumum_length()
Eliminate words that do not meet the minimum length criteria.
f.	Extract integer value: get_int_from_str()
To extract integer value from strings. Used for extracting document ids from document names.
2.	corpusHandler class:
a.	Process the corpora: process_collection()
Processes the files in the corpora directory, extracts the title and text contents alone for each file using BeautifulSoup package, initiates the inverted index construction.
b.	Building the data structure:build_term_frequency()
Builds the inverted index data structure. The general structure of the dictionary object being constructed is as follows:
{
token1: {
	df: document_frequency,
	tf:{
		doc_id_1: term_frequency_1,
		doc_id_2: term_frequency_2
	   }
	}
}
c.	Generating document lengths: generate_doc_length()
Performs a second pass over all the documents and generates the document length for each document. This value is utilized later to calculate the cosine similarity between the query and the document.
3.	queryHandler class:
a.	Get relevance details: readRelevance()
Read and store the relevance details for each query in order to generate the precision and recall metrics.
b.	Process queries: process_queries()
Reads the queries one by one from the queries file, initiates the cosine similarity calculation and performs ranking. It also initiates the generation of the output.
c.	Calculate cosine similarity: generate_cosine_similarity()
Generates cosine similarity by incrementally calculating the product of the weights for each term in the query with the relevant documents.
d.	Generate metrics: calculate_metrics()
Calculates the precision and recall for the given cosine similarity of each query at ranks 10, 50, 100 and 500. The ranks are hardcoded.
e.	Output generation: pretty_print()
Generate the output in the required format. It is directed to the default output stream.

Results:
Evaluating your queries...
Top 10 documents in rank list
Query:  1 	Pr:  0.0 	Re:  0.0
Query:  2 	Pr:  0.2 	Re:  0.13333333333333333
Query:  3 	Pr:  0.2 	Re:  0.13333333333333333
Query:  4 	Pr:  0.1 	Re:  0.05555555555555555
Query:  5 	Pr:  0.1 	Re:  0.05263157894736842
Query:  6 	Pr:  0.4 	Re:  0.2222222222222222
Query:  7 	Pr:  0.6 	Re:  0.6666666666666666
Query:  8 	Pr:  0.2 	Re:  0.5
Query:  9 	Pr:  0.0 	Re:  0.0
Query:  10 	Pr:  0.2 	Re:  0.08333333333333333


Avg precision: 0.2
Avg recall: 0.18470760233918126

Top 50 documents in rank list
Query:  1 	Pr:  0.0 	Re:  0.0
Query:  2 	Pr:  0.12 	Re:  0.4
Query:  3 	Pr:  0.12 	Re:  0.4
Query:  4 	Pr:  0.04 	Re:  0.1111111111111111
Query:  5 	Pr:  0.14 	Re:  0.3684210526315789
Query:  6 	Pr:  0.14 	Re:  0.3888888888888889
Query:  7 	Pr:  0.16 	Re:  0.8888888888888888
Query:  8 	Pr:  0.06 	Re:  0.75
Query:  9 	Pr:  0.12 	Re:  0.75
Query:  10 	Pr:  0.08 	Re:  0.16666666666666666


Avg precision: 0.098
Avg recall: 0.4223976608187135

Top 100 documents in rank list
Query:  1 	Pr:  0.0 	Re:  0.0
Query:  2 	Pr:  0.09 	Re:  0.6
Query:  3 	Pr:  0.09 	Re:  0.6
Query:  4 	Pr:  0.06 	Re:  0.3333333333333333
Query:  5 	Pr:  0.12 	Re:  0.631578947368421
Query:  6 	Pr:  0.09 	Re:  0.5
Query:  7 	Pr:  0.09 	Re:  1.0
Query:  8 	Pr:  0.03 	Re:  0.75
Query:  9 	Pr:  0.06 	Re:  0.75
Query:  10 	Pr:  0.04 	Re:  0.16666666666666666


Avg precision: 0.06699999999999999
Avg recall: 0.5331578947368422

Top 500 documents in rank list
Query:  1 	Pr:  0.002 	Re:  1.0
Query:  2 	Pr:  0.03 	Re:  1.0
Query:  3 	Pr:  0.03 	Re:  1.0
Query:  4 	Pr:  0.032 	Re:  0.8888888888888888
Query:  5 	Pr:  0.038 	Re:  1.0
Query:  6 	Pr:  0.034 	Re:  0.9444444444444444
Query:  7 	Pr:  0.018 	Re:  1.0
Query:  8 	Pr:  0.008 	Re:  1.0
Query:  9 	Pr:  0.016 	Re:  1.0
Query:  10 	Pr:  0.026 	Re:  0.5416666666666666


Avg precision: 0.0234
Avg recall: 0.9375
