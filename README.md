### Langauge Model and Word Embedding
In this project, we implement a N-gram Model and two word embedding modes based on Glove and Word2vec. We use these models to realize test text classification between Obama and Trump.
The training sets are collected from speeches of Obama and Trump.

Assignment1_resources contain traning sets and test sets. The new analogy test cases are also included.

src:

- preprocessor.py splits the whole speech into tokens.
- ngram.py implements a N-Gram model receiving a parameter n.
- word_embedding implements two models based on Glove and Word2vec.
- speech_classification uses N-Gram model to classify the test speech.
