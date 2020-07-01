# Search_Engine_Sinhala_Lyrics

## data
Contains data added to elastic search cluster.
* mapping.json : custom mapping object
* sinhala_songs_corpus.json : data before processing
* sinhala_songs.bulk : Data after processing

## lambda function

Includes the implementation for AWS lambda function. Generate elastic query. 

## scripts 
* curl_scripts.txt : contains curl commands for Creating, Updating, Deleting, and Searching data in elastic cluster.
* search_songs.js : Process user query and call API endpoint.

## Other Files 
* FastText_Generator_Gensim.ipynb : Implementation for fasttext model used to generate similar words.
* format_data_for_es.py : Process data before posting to elastic search cluster.
* index.html : GUI for search application. 