# Search Engine Experimentation Project

The purpose of this Python project is to experiment with different Natural Language Processing techniques using a test dataset of HTML pages. The Search Engine program runs a Tkinter GUI where the user can input queries and view the results of the query in an ouput box. The currently implemented ranking algorithms are TF-IDF, Vector Space (using Cosine Similarity), and BM25. Additional NLP techniques that have been implemented include: Stop Words, Tag Weighting, Stemming, Lemmatization, Query Expansion, and Named Entity Recognition. The HTML test data I used was based around Video Games.

# Dependencies

- Python 3.13.9
- Beautiful Soup 4 --> ``` pip install bs4 ```
- NLTK --> ``` pip install nltk ```
- spaCy --> ``` pip install spacy ```

# How To Use

- Download the project.
  
- Install the dependencies.

- Navigate to the main project directory.
  
- Replace the data in the ``` test_data ``` directory with your own set of HTML documents, or use the existing data. A large dataset is recommended for testing queries.
  
- Run ``` python main.py ``` once to create the index, this may take a while depending on the dataset size.
  
- The message ``` New Index Saved ``` will be outputted when the index has finished being created.

- Now, each time the program is run with ``` python main.py ```, it should launch the GUI.

- Within the GUI, enter queries into the input box below ``` Enter Query: ```. Then press ``` Run Query ``` so the program can process the query and return relevant documents in the dataset. The results will appear in the text box below ``` Query Result: ```.

- The default ranking algorithm used is TF-IDF. To switch between ranking algorithms, press the corresponding button on the right side of the screen. The currently used ranking algorithm is also displayed.

- To replace the current index with a new dataset, run ``` python main.py new ``` after replacing the files in the ``` test_data ``` directory.

# Notes

- By default, the additional NLP methods used by the Search Engine are Stop Words, Lemmatization, and Query Expansion. These methods can be enabled/disabled in the file ``` tokenizor.py ```. Changing these methods for Document Tokenization (not Query Tokenization) requires a new index to be created for it to take effect.

- Tag Weights can be found and edited in the file ``` rankings/tf_idf.py ```. These can be changed without having to create a new index.
