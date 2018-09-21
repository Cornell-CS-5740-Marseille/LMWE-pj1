import math
import random
import json

from src.preprocessor import preprocessor
from src.ngram import Ngrams

class speech_classification:
    def __init__(self, trained_data): #input is array
        self.data = trained_data

    def get_model(self):
        self.ngram = Ngrams({"n": 1, "threshold": 100})

    def compute(self):
        test_list = self.data
        for x in range(0, len(test_list) - self.ngram.n + 1):
            key = self.to_key(test_list[x: x + self.ngram.n - 1]) if self.ngram.n > 1 else self.placeholder
            target = test_list[x + self.ngram.n - 1]

speech_classification.get_model()
