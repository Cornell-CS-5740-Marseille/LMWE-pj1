import csv
from collections import defaultdict

import numpy as np
import gensim
from glove import Glove

from sklearn.feature_extraction.text import TfidfVectorizer

from src.preprocessor import preprocessor


class word_embedding_model:
    def __init__(self, trained_file):
        self.vec_dict = {}
        self.dim = 300
        self.trainedVector = {}

    def word_embedding(self, tokens):
        vector = np.zeros(self.dim)
        return vector

    def trainSpeechVector(self, speech, name):
        vector = np.zeros(self.dim)
        for sentence in speech:
            vector = np.add(vector, self.word_embedding(sentence))
        self.trainedVector[name] = np.divide(vector, len(speech))

    def classification(self, sentence):
        vector = self.word_embedding(sentence)
        distance_obama = np.linalg.norm(vector - self.trainedVector["obama"])
        distance_trump = np.linalg.norm(vector - self.trainedVector["trump"])
        if distance_obama > distance_trump:
            return 1
        elif distance_trump > distance_obama:
            return 0
        else:
            return 0

    def testData(self, data, saveFile):
        with open('../output/' + saveFile, mode='w') as speech_output:
            speech_writer = csv.writer(speech_output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            speech_writer.writerow(['Id', 'Prediction'])
            for i in range(len(data)):
                speech_writer.writerow([i, self.classification(data[i])])


class glove(word_embedding_model):
    def __init__(self, trained_file):
        self.dim = 50
        self.glove = Glove().load_stanford(trained_file)
        self.trainedVector = {}

    def word_embedding(self, sentence):
        vector = np.zeros(self.dim)
        num = 0
        for word in sentence:
            if word not in self.glove.dictionary:
                continue
            vector = np.add(vector, self.glove.word_vectors[self.glove.dictionary[word]])
            num = num + 1
        result = np.divide(vector, num)
        return result


    def analogy_test(self, test_file):
        correct, total, missed = 0, 0, 0
        with open(test_file, 'r') as file:
            for line in file:
                words = map(lambda x: x.lower(), line.strip().split(" "))
                vector = self.glove.word_vectors[self.glove.dictionary[words[1]]] + self.glove.word_vectors[self.glove.dictionary[words[2]]] - self.glove.word_vectors[self.glove.dictionary[words[0]]]
                total += 1
                similar_words = self.glove._similarity_query(vector.tolist(), 5)
                if similar_words[0][0] == words[3]:
                    correct += 1
                else:
                    missed += 1

        return correct, total, missed



class word2vec(word_embedding_model):
    def __init__(self, trained_file):
        self.word2vec = gensim.models.KeyedVectors.load_word2vec_format(trained_file, binary=True)
        self.dim = 300
        self.trainedVector = {}

    def analogy_test(self, test_file):
        correct, total, missed = 0, 0, 0
        with open(test_file, 'r') as file:
            for line in file:
                words = map(lambda x: x.lower(), line.strip().split(" "))
                total += 1
                similar_words = self.word2vec.most_similar(positive=[words[1], words[2]], negative=[words[0]])
                if similar_words[0][0] == words[3]:
                    correct += 1
                else:
                    missed += 1

        return correct, total, missed

    def fit(self, X, y = 0):
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(X)
        # if a word was never seen - it must be at least as infrequent
        # as any of the known words - so the default idf is the max of
        # known idf's
        max_idf = max(tfidf.idf_)
        self.word2weight = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return self

    def word_embedding(self, sentence):
        vector = np.zeros(self.dim)
        num = 0
        for word in sentence:
            if word not in self.word2vec:
                continue
            vector = np.add(vector, self.word2vec.wv[word])
            num += 1
        final_vector = np.divide(vector, num)
        return final_vector






# glove = glove("../Assignment1_resources/trained_data/glove.6B.50d.txt")
# trump_data = preprocessor("../Assignment1_resources/train/trump.txt", 0).data[4]
# obama_data = preprocessor("../Assignment1_resources/train/obama.txt", 0).data[4]
# glove.trainSpeechVector(trump_data, "trump")
# glove.trainSpeechVector(obama_data, "obama")
# test_data = preprocessor("../Assignment1_resources/test/test.txt", 0).data[4]
# glove.testData(test_data, "speech_classification_glove.txt")
# analogy test
# glove.analogy_test("../Assignment1_resources/analogy_test.txt")


word2vec_model = word2vec("../Assignment1_resources/trained_data/GoogleNews-vectors-negative300.bin")
trump_data = preprocessor("../Assignment1_resources/train/trump.txt", 0).data[4]
obama_data = preprocessor("../Assignment1_resources/train/obama.txt", 0).data[4]
word2vec_model.trainSpeechVector(trump_data, "trump")
word2vec_model.trainSpeechVector(obama_data, "obama")
test_data = preprocessor("../Assignment1_resources/test/test.txt", 0).data[4]
word2vec_model.testData(test_data, "speech_classification_word2vec.txt")

# analogy test
# print word2vec_model.analogy_test("../Assignment1_resources/analogy_test.txt")
