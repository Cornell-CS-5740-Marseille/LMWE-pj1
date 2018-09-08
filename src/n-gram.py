import random
class Ngrams:
    def __init__(self, opts):
        self.n = opts["n"]
        self.start_symbol = "<s>"
        self.end_symbol = "</s>"
        self.unknown_symbol = "<u>"
        self.placeholder = " "
        self.count_table = {}
        self.threshold = opts["threshold"]

    def to_key(self, prefix):
        return "-".join(prefix)

    def dist_table(self, logs):
        n = self.n
        for log in logs:
            for i in range(0, len(log) - n + 1):
                if n > 1:
                    key = self.to_key(log[i: i+n-1])
                else:
                    key = self.placeholder
                target = log[i+n-1]
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
            for target in self.count_table[key]:
                self.count_table[key][target] /= (number + 0.0)
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
            sequence = sentence[i: i+n-1] if n > 1 else []
            target = sentence[i+n-1]
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
            print "round " , x, key, start
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
                return sentence
        return sentence
# test cases
corpus = ["<s> I am Sam </s>".split(" "), "<s> Sam I am </s>".split(" "), "<s> I do not like green eggs and ham </s>".split(" ")]
ngram = Ngrams({"n": 2, "threshold": 100})
print ngram.dist_table(corpus)
# print ngram.unsmoothed_nGram("<s> I am </s>")
print ngram.sentence('I')