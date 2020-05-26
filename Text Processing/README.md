Aim: Perform a variety of text processing operations on a data corpus and generate basic statistics.
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
<br>
<b>Executing the source code - Input arguments:</b>
<ul>
  <li>The source code can be executed without any input arguments.</li>
  <li>By default, the implementation looks for a directory named ‘citeseer’ and processes all documents in the directory. If the directory is unavailable, it tries to extract contents from ‘citeseer.zip’ (intending to result in a directory named ‘citeseer’). If both operations fail, the source code exits.</li>
  <li>If the end-user seeks to utilize a different directory, the full path can be provided as the first argument while running the code.
    <br>
    >> python main.py full_path_of_directory
    </li>
    <li>If the end-user seeks to provide a zip file name (to be extracted), it can be provided as the first argument while running the code along with the directory name to be processed as the second argument.
      <br>
      >> python main.py full_path_of_zip_file directory_name
      <br>
      Note: The files will be extracted to the current directory of the source code.
    </li>
</ul>
<br>
<b>Execution outputs:</b>
<ul>
  <li>The execution results in two sets of results, one without stop words removal and stemming and the other with both applied to the texts.</li>
  <li>All results are directed to the default command line output stream.</li>
  <li>Each set of results consist of the following:
    <ul>
      <li>Total number of words in the collection: An integer value</li>
      <li>Vocabulary size: An integer value</li>
      <li>Top 20 words in the collection: A list of top 20 words with their corresponding frequencies.</li>
      <li>Stop words in the top 20 words in the collection: A list of stop words in the top 20 words with their corresponding frequencies. If no stop words are present, the text "&lt;&lt;No stop words available&gt;&gt;" is displayed instead.</li>
      <li>The minimum number of unique words corresponding to 15% of the total number of words in the collection: An integer value, along with the list of such words.</li>
    </ul>
  </li>
</ul>
<br>
<b>Functionalities:</b>
<br>
The source consists of a class ‘textProcessor’ which encapsulates all the required functionalities. It is initiated using the directory name to be processed and makes a single pass over all the documents in the directory, processes the text and generates the following results.
<ol>
  <li>term_frequency: Hash table (dict in Python) holding the term frequency of the vocabulary</li>
  <li>collection_size: the total number of words in the collection</li>
</ol>

The various functionalities are as follows:
<ol>
  <li>Punctuation removal: remove_punctuation()
    <br>
    All punctuations in the text are removed prior to tokenization. This will result in the tokenization of a sentence of the form “These are Mary’s shoes” into [these, are, marys, shoes] instead of [these, are, mary, s, shoes].
  </li>
  <li>Tokenization: tokenize_str()
    <br>
    The text is stripped of trailing or preceding white spaces, converted to lower case, processed by the punctuation removal module, and tokenized based on the white space.
    <br>
    Note: As part of the tokenization process, the numbers (Ex: 1, 243) are not removed from the text.
  </li>
  <li>Text processor: preprocessor()
    <br>
    This module encapsulates a number of smaller functionalities.
    <ul>
      <li>Initially, the tokenization module is invoked using the text.</li>
      <li>If stop words are to be eliminated, the list of stop words available in the NLTK package are utilized to identify and eliminate them.</li>
      <li>If the stemmer is enabled, the Porter Stemmer from the NLTK package is utilized to stem each word.</li>
      <li>The size of the collection is updated.</li>
      <li>The term frequency data is updated.</li>
    </ul>
  </li>
  <li>Collection processor: process_collection()
    <br>
    Parses every single file in the given directory, invokes the text processor and finally sorts the term frequency data in the decreasing order of frequencies.
  </li>
  <li>Top N words: top_N_keys()
    <br>
    Identifies the top N words ranked based on their frequencies.
  </li>
  <li>Percentage identifier: top_percentage_counter()
    <br>
    Identifies the number of words making up X% of the total collection size, where X is provided as an argument.
  </li>
</ol>
<br>
<b>Results:</b>
<br>
Text processing WITHOUT Stemming and stop word removal
<br>
Total number of words in the collection: 476263
<br>
Vocabulary size: 19885
<br>

<br>Top 20 words in the collection:
<br>the 	 	25662
<br>of 		18638
<br>and 	 	14131
<br>a 	 	13345
<br>to 	 	11536
<br>in 	 	10067
<br>for 	 	7379
<br>is 	 	6577
<br>we 	 	5138
<br>that 	 	4820
<br>this 	 	4446
<br>are 	 	3737
<br>on 	 	3656
<br>an 	 	3281
<br>with 	 	3200
<br>as 	 	3057
<br>by 	 	2765
<br>data 	 	2691
<br>be 	 	2500
<br>information 	2322

<br>Stop words in top 20 words in the collection:
<br>the 	 	25662
<br>of 		18638
<br>and 	 	14131
<br>a 	 	13345
<br>to 	 	11536
<br>in 	 	10067
<br>for 	 	7379
<br>is 	 	6577
<br>we 	 	5138
<br>that 	 	4820
<br>this 	 	4446
<br>are 	 	3737
<br>on 	 	3656
<br>an 	 	3281
<br>with 	 	3200
<br>as 	 	3057
<br>by 	 	2765
<br>be 	 	2500

<br>Minimum number of unique words accounting for 15% of total number of words in the collection: 4
<br>Top 4 words in the collection:
<br>the 	 	25662
<br>of 		18638
<br>and 	 	14131
<br>a 	 	13345

<br>Text processing WITH Stemming and stop word removal
<br>Total number of words in the collection: 294191
<br>Vocabulary size: 13777
<br>Top 20 words in the collection:
<br>system	3741
<br>use 	 	3740
<br>data 	 	2691
<br>agent 	 	2688
<br>inform 	 	2398
<br>model 	 	2315
<br>paper 	 	2246
<br>queri 	 	1905
<br>user 	 	1756
<br>learn 	 	1740
<br>algorithm 	1584
<br>1 	 	1552
<br>approach	1544
<br>problem 	1543
<br>applic 	 	1522
<br>present	1507
<br>base 	 	1486
<br>web 	 	1439
<br>databas 	1424
<br>comput 	1411

<br>Stop words in top 20 words in the collection:  &lt;&lt;No stop words available&gt;&gt;

<br>Minimum number of unique words accounting for 15% of total number of words in the collection: 24
<br>Top 24 words in the collection:
<br>system	3741
<br>use 	 	3740
<br>data 	 	2691
<br>agent 	 	2688
<br>inform 	 	2398
<br>model 	 	2315
<br>paper 	 	2246
<br>queri 	 	1905
<br>user 	 	1756
<br>learn 	 	1740
<br>algorithm 	1584
<br>1 	 	1552
<br>approach	1544
<br>problem 	1543
<br>applic 	 	1522
<br>present	1507
<br>base 	 	1486
<br>web 	 	1439
<br>databas 	1424
<br>comput 	1411
<br>method 	1223
<br>result 	 	1202
<br>provid 	 	1185
<br>design 	 	1160
