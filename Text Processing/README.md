Source code name: slaksh5_hw1.py
Programming language: Python 3.7.1

Package dependencies:
1.	os: to perform file operations
2.	sys: to read input arguments
3.	string: to handle punctuations in the text
4.	zipfile: to extract contents from the zip file
5.	nltk: to perform text processing operations

Executing the source code - Input arguments:
●	The source code can be executed without any input arguments.
●	By default, the implementation looks for a directory named ‘citeseer’ and processes all documents in the directory. If the directory is unavailable, it tries to extract contents from ‘citeseer.zip’ (intending to result in a directory named ‘citeseer’). If both operations fail, the source code exits.
●	If the end-user seeks to utilize a different directory, the full path can be provided as the first argument while running the code.
Ex:
>> python slaksh5_hw1.py <full_path_of_directory>
●	If the end-user seeks to provide a zip file name (to be extracted), it can be provided as the first argument while running the code along with the directory name to be processed as the second argument.
Ex:
>> python slaksh5_hw1.py <full_path_of_zip_file> <directory_name>
Note: The files will be extracted to the current directory of the source code.

Execution outputs:
●	The execution results in two sets of results, one without stop words removal and stemming and the other with both applied to the texts.
●	All results are directed to the default command line output stream.
●	Each set of results consist of the following:
○	Total number of words in the collection: An integer value
○	Vocabulary size: An integer value
○	Top 20 words in the collection: A list of top 20 words with their corresponding frequencies.
○	Stop words in the top 20 words in the collection: A list of stop words in the top 20 words with their corresponding frequencies. If no stop words are present, the text “<<No stop words available>>” is displayed instead.
○	The minimum number of unique words corresponding to 15% of the total number of words in the collection: An integer value, along with the list of such words.

Functionalities:
The source consists of a class ‘textProcessor’ which encapsulates all the required functionalities. It is initiated using the directory name to be processed and makes a single pass over all the documents in the directory, processes the text and generates the following results.
1.	term_frequency: Hash table (dict in Python) holding the term frequency of the vocabulary
2.	collection_size: the total number of words in the collection

The various functionalities are as follows:
1.	Punctuation removal: remove_punctuation()
All punctuations in the text are removed prior to tokenization. This will result in the tokenization of a sentence of the form “These are Mary’s shoes” into [these, are, marys, shoes] instead of [these, are, mary, s, shoes].
2.	Tokenization: tokenize_str()
The text is stripped of trailing or preceding white spaces, converted to lower case, processed by the punctuation removal module, and tokenized based on the white space.
Note: As part of the tokenization process, the numbers (Ex: 1, 243) are not removed from the text.
3.	Text processor: preprocessor()
This module encapsulates a number of smaller functionalities.
a.	Initially, the tokenization module is invoked using the text.
b.	If stop words are to be eliminated, the list of stop words available in the NLTK package are utilized to identify and eliminate them.
c.	If the stemmer is enabled, the Porter Stemmer from the NLTK package is utilized to stem each word.
d.	The size of the collection is updated.
e.	The term frequency data is updated.
4.	Collection processor: process_collection()
Parses every single file in the given directory, invokes the text processor and finally sorts the term frequency data in the decreasing order of frequencies.
5.	Top N words: top_N_keys()
Identifies the top N words ranked based on their frequencies.
6.	Percentage identifier: top_percentage_counter()
Identifies the number of words making up X% of the total collection size, where X is provided as an argument.

 
Results:
Text processing WITHOUT Stemming and stop word removal
Total number of words in the collection: 476263
Vocabulary size: 19885

Top 20 words in the collection:
the 	 	25662
of 		18638
and 	 	14131
a 	 	13345
to 	 	11536
in 	 	10067
for 	 	7379
is 	 	6577
we 	 	5138
that 	 	4820
this 	 	4446
are 	 	3737
on 	 	3656
an 	 	3281
with 	 	3200
as 	 	3057
by 	 	2765
data 	 	2691
be 	 	2500
information 	2322


Stop words in top 20 words in the collection:
the 	 	25662
of 		18638
and 	 	14131
a 	 	13345
to 	 	11536
in 	 	10067
for 	 	7379
is 	 	6577
we 	 	5138
that 	 	4820
this 	 	4446
are 	 	3737
on 	 	3656
an 	 	3281
with 	 	3200
as 	 	3057
by 	 	2765
be 	 	2500

Minimum number of unique words accounting for 15% of total number of words in the collection: 4
Top 4 words in the collection:
the 	 	25662
of 		18638
and 	 	14131
a 	 	13345

Text processing WITH Stemming and stop word removal
Total number of words in the collection: 294191
Vocabulary size: 13777
Top 20 words in the collection:
system	3741
use 	 	3740
data 	 	2691
agent 	 	2688
inform 	 	2398
model 	 	2315
paper 	 	2246
queri 	 	1905
user 	 	1756
learn 	 	1740
algorithm 	1584
1 	 	1552
approach	1544
problem 	1543
applic 	 	1522
present	1507
base 	 	1486
web 	 	1439
databas 	1424
comput 	1411

Stop words in top 20 words in the collection:  <<No stop words available>>

Minimum number of unique words accounting for 15% of total number of words in the collection: 24
Top 24 words in the collection:

system	3741
use 	 	3740
data 	 	2691
agent 	 	2688
inform 	 	2398
model 	 	2315
paper 	 	2246
queri 	 	1905
user 	 	1756
learn 	 	1740
algorithm 	1584
1 	 	1552
approach	1544
problem 	1543
applic 	 	1522
present	1507
base 	 	1486
web 	 	1439
databas 	1424
comput 	1411
method 	1223
result 	 	1202
provid 	 	1185
design 	 	1160



