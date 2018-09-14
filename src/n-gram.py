import math
import random
import json

from src.preprocessor import preprocessor

class Ngrams:
    # Initialization method
    def __init__(self, opts):
        self.n = opts["n"]  # length of n-gram (trigram: n=3)
        self.start_symbol = "<s>"  # start of document
        self.end_symbol = "</s>"  # end of document
        self.unknown_symbol = "<u>"  # unknown n-gram
        self.placeholder = " "  # buffer used in case of short prefix (?)
        self.count_table = {}   # data structure for the n-gram count; dict<string, dict<string, double>>
        self.threshold = opts["threshold"]  # max number of words in teh sentence generation

        # for smoothing
        self.all_count_symbol = "<a>"  # counter for each key
        self.other_symbol = "<o>"  # unknown n-gram
        self.all_unique_pair_counter = 0  # counter for all n-gram pairs
        self.discount = 0.02  # discount value to be used in kneser-ney
        self.all_tokens = set({self.start_symbol, self.end_symbol})
        self.smoothed_count_table = {}  # data structure for the smoothed n-gram count; dict<string, dict<string, double>>
        self.reverse_dict = {}

    def to_key(self, prefix):               # convert a string to a dictionary key
        return "-".join(prefix)

    # create the count table with raw frequencies at first
    def dist_table(self, logs):
        n = self.n
        # add each occurrance of n-gram into the dictionary. The key is the
        # (n-1)-gram and the value is another dictionary of each words' frequency
        # following that (n-1)-gram
        for log in logs:
            for i in range(0, len(log) - n + 1):
                if n > 1:
                    key = self.to_key(log[i: i + n - 1])
                else:
                    key = self.placeholder
                target = log[i + n - 1]
                if key in self.count_table:
                    if target in self.count_table[key]:
                        self.count_table[key][target] += 1
                    else:
                        self.count_table[key][target] = 1
                else:
                    self.count_table[key] = {target: 1}

        for key in self.count_table:
            count_dict = self.count_table[key]
            number = reduce((lambda x, y: x + y), count_dict.values())
            for target in count_dict:
                count_dict[target] /= (number + 0.0)

        return self.count_table

    def dist_table_smoothed(self, logs):
        n = self.n
        for log in logs:
            for i in range(0, len(log) - n + 1):
                if n > 1:
                    key = self.to_key(log[i: i + n - 1])
                else:
                    key = self.placeholder
                target = log[i + n - 1]
                self.all_tokens.add(target)

                # count table
                if key in self.count_table:
                    if target in self.count_table[key]:
                        self.count_table[key][target] += 1
                    else:
                        self.count_table[key][target] = 1
                    self.count_table[key][self.all_count_symbol] += 1
                else:
                    self.count_table[key] = {target: 1}
                    self.count_table[key][self.all_count_symbol] = 1

                # reverse count table
                if target in self.reverse_dict:
                    if key in self.reverse_dict[target]:
                        self.reverse_dict[target][key] += 1
                    else:
                        self.reverse_dict[target][key] = 1
                    self.reverse_dict[target][self.all_count_symbol] += 1
                else:
                    self.reverse_dict[target] = {key: 1}
                    self.reverse_dict[target][self.all_count_symbol] = 1

        for key in self.count_table:
            self.all_unique_pair_counter += len(self.count_table[key]) - 1  # minus the <a> in the dict

        for key in self.count_table:
            self.smoothed_count_table[key] = {}
            remaining_prob = 1
            count_dict = self.count_table[key]
            for target in count_dict:  # yeah i know, this is super slow OMG
                if target != self.all_count_symbol:
                    count = 0
                    if target in count_dict:
                        count = count_dict[target]
                    percentage_after_discount = max(count - self.discount, 0) / \
                                                (count_dict[self.all_count_symbol] + 0.0)
                    normalized = self.discount * len(count_dict) / (count_dict[self.all_count_symbol] + 0.0)
                    reverse_count = 0
                    if target in self.reverse_dict:
                        reverse_count = len(self.reverse_dict[target]) - 1
                    prev = reverse_count / (self.all_unique_pair_counter + 0.0)
                    smoothed_prob = percentage_after_discount + normalized * prev
                    self.smoothed_count_table[key][target] = smoothed_prob
                    remaining_prob -= smoothed_prob
            self.smoothed_count_table[key][self.other_symbol] = remaining_prob
        self.count_table = self.smoothed_count_table
        return self.count_table

    def lookup_dist(self, sequence, target):
        n = self.n
        key = self.to_key(sequence) if n > 1 else self.placeholder
        if key in self.count_table:
            return self.count_table[key][target] if target in self.count_table[key] else 0
        else:
            return 0

    def unsmoothed_nGram(self, sentence):
        sentence = sentence.split(" ")
        n = self.n
        probability = 1
        for i in range(0, len(sentence) - n + 1):
            sequence = sentence[i: i + n - 1] if n > 1 else []
            target = sentence[i + n - 1]
            prob = self.lookup_dist(sequence, target)
            probability *= prob

        return probability

    def sentence(self, prefix):
        # assume that length of prefix is larger than n
        sentence = prefix
        prefix = prefix.split(' ') if len(prefix) > 0 else []
        if len(prefix) >= self.n - 1:
            start = prefix[len(prefix) - self.n:]
        else:
            start = ["<s>"]
        for x in range(0, self.threshold):
            key = self.to_key(start) if self.n > 1 else self.placeholder
            print "round ", x, key, start
            if key in self.count_table:
                prob = random.uniform(0, 1)
                items = self.count_table[key].items()
                lower = 0
                for target, probability in items:
                    if prob >= lower and prob < probability + lower:
                        sentence = sentence + " " + target
                        start.append(target)
                        start = start[1:]
                        print start, sentence
                        break
                    else:
                        lower += probability
            else:
                print "no key:", key
                return sentence
        return sentence

    def perplexity(self, test_list):
        exponent = 0
        n = self.n
        for x in range(0, len(test_list) - n + 1):
            key = self.to_key(test_list[x: x + n - 1]) if n > 1 else self.placeholder
            target = test_list[x + n - 1]
            exponent = exponent - math.log(self.lookup_dist(key, target))

        exponent /= (len(test_list) - n + 1.0)
        PP = math.exp(exponent)
        return PP

    def save_model(self, file):
        fileName = file + "-" + str(self.n) + ".json"
        with open(fileName, 'w') as fp:
            json.dump(self.count_table, fp)


# test cases
# corpus = ["<s> I am Sam </s>".split(" "), "<s> Sam I am </s>".split(" "), "<s> I do not like green eggs and ham </s>".split(" ")]
# ngram = Ngrams({"n": 2, "threshold": 100})
# print ngram.dist_table(corpus)
# print ngram.sentence('I')

data = preprocessor("../Assignment1_resources/train/obama.txt").data

ngram = Ngrams({"n": 3, "threshold": 100})

ngram.dist_table_smoothed([data[0]])
print ngram.smoothed_count_table["and-then"]

#ngram.save_model("model/trump")
#print ngram.sentence('I')
