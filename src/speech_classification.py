import math
import random
import json
import csv

from src.preprocessor import preprocessor
from src.ngram import Ngrams

class speech_classification:
    def __init__(self):
        return

    def get_model(self, n, threshold):
        return Ngrams({"n": n, "threshold": threshold})

    def compute(self, data, ngram):  # the smaller total_log_prob is, the more probable the sentence is
        total_log_prob_arr = [];
        for i in range(len(data)):
            test_sentence = data[i]
            total_log_prob = 0
            for x in range(0, len(test_sentence) - ngram.n + 1):
                key = ngram.to_key(test_sentence[x: x + ngram.n - 1]) if ngram.n > 1 else ngram.placeholder
                target = test_sentence[x + ngram.n - 1]
                log_prob = math.log(ngram.lookup_dist(key, target)) if ngram.lookup_dist(key, target) > 0 else 0
                total_log_prob -= log_prob
            total_log_prob_arr.append(total_log_prob)
        return total_log_prob_arr

    def classify(self):
        obama_model = preprocessor("../Assignment1_resources/train/obama.txt", 0).data
        trump_model = preprocessor("../Assignment1_resources/train/trump.txt", 0).data
        test_data = (preprocessor("../Assignment1_resources/test/test.txt", 0).data)[5]
        ngram_obama = self.get_model(3, 100)
        ngram_trump = self.get_model(3, 100)
        ngram_obama.dist_table_smoothed_kneser_ney(obama_model)
        ngram_trump.dist_table_smoothed_kneser_ney(trump_model)
        #ngram_obama.dist_table_add_one_smooth(obama_model, 2)
        #ngram_trump.dist_table_add_one_smooth(trump_model, 2)
        #print ngram_obama.count_table
        obama_arr = self.compute(test_data, ngram_obama)
        trump_arr = self.compute(test_data, ngram_trump)
        result_arr = []

        for i in range(len(obama_arr)):
            if obama_arr[i] < trump_arr[i]:
                result_arr.append('0')
            else:
                result_arr.append('1')

        with open('../output/speech_classification.csv', mode='w') as speech_output:
            speech_writer = csv.writer(speech_output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            speech_writer.writerow(['Id', 'Prediction'])
            for i in range(len(result_arr)):
                speech_writer.writerow([i, result_arr[i]])

        #print result_arr


my_speech_classification = speech_classification()
my_speech_classification.classify()