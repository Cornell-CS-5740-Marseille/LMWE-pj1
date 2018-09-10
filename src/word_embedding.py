import array

import gensim
import numpy as np
from glove import Glove


class word_embedding_model:
    def __init__(self, trained_file):
        self.vec_dict = {}


class glove(word_embedding_model):
    def __init__(self, trained_file):
        self.length = 300
        self.glove = Glove().load_stanford(trained_file)
        # dct = {}
        # vectors = array.array('d')
        # with open(trained_file) as file:
        #     for i, line in enumerate(file):
        #         vector_list = line.split(' ')
        #         word = vector_list[0]
        #         vector = map(lambda x: float(x), vector_list[1:])
        #         print word, len(vector)
        #
        #         if len(vector) != self.length:
        #             continue
        #         dct[word] = i
        #         vectors.extend(float(x) for x in vector)
        #     no_vectors = len(dct)
        #     self.glove.word_vectors = (np.array(vectors)
        #                          .reshape(no_vectors,
        #                                   self.length))
        #     self.glove.add_dictionary(dct)
        print "dasd"

    def word_embedding(self, tokens):
        vector = [0] * self.length
        length = 0
        for word in tokens:
            if word in self.vec_dict:
                for x in range(0, len(vector)):
                    vector[x] += self.vec_dict[word][x]
                length += 1
        result = map(lambda i: float(i) / length, vector)
        return result



    def analogy_test(self, test_file):
        correct, total, missed = 0, 0, 0
        with open(test_file, 'r') as file:
            for line in file:
                words = map(lambda x: x.lower(), line.strip().split(" "))
                vector = self.glove.word_vectors[self.glove.dictionary[words[1]]] + self.glove.word_vectors[self.glove.dictionary[words[2]]] - self.glove.word_vectors[self.glove.dictionary[words[0]]]
                # print self.glove.dictionary[words[1]], self.glove.word_vectors[self.glove.dictionary[words[1]]]
                total += 1
                similar_words = self.glove._similarity_query(vector.tolist(), 5)
                print words[3], similar_words[0][0]
                if similar_words[0][0] == words[3]:
                    correct += 1
                else:
                    missed += 1

        return correct, total, missed



class word2vec(word_embedding_model):
    def __init__(self, trained_file):
        self.word2vec = gensim.models.KeyedVectors.load_word2vec_format(trained_file, binary=True)

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

glove = glove("../Assignment1_resources/trained_data/glove.6B.50d.txt")
glove.analogy_test("../Assignment1_resources/analogy_test.txt")
# word2vec_model = word2vec("../Assignment1_resources/trained_data/GoogleNews-vectors-negative300.bin")
# print word2vec_model.analogy_test("../Assignment1_resources/analogy_test.txt")
