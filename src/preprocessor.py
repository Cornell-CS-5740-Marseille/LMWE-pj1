# coding=utf-8
import re


class preprocessor:
    def __init__(self, file):
        self.unknown_symbol = "<u>"
        self.unknown_threshold = 1
        with open(file) as f:
            self.data = self.data_processor(f)

    def data_processor(self, fhandle):
        ls = list()
        result = list()
        unknown_list = dict()
        dictionary = set()

        for line in fhandle:
            line_new = line.replace('’','\'')
            line_new = line_new.replace('``','\"')
            line_new = line_new.replace('\'\'','\"')
            line_new = line_new.replace('\' ','\'')
            line_new = line_new.replace('”','\"')
            line_new = line_new.replace('“','\"')
            line_new = line_new.replace('\n', '')
            # ls[0] = ls[0].capitalize()
            # for i in range(len(ls)-1):
            #     if ls[i] == '.':
            #         ls[i+1] = ls[i+1].capitalize()
            # line_new = ' '.join(ls) + '\n'
            # line_new = line_new.replace(' i ',' I ')
            ls = line_new.split(" ")
            for x in range(len(ls)):
                word = ls[x]
                new_word = word.rstrip('?:!.,;')
                new_list = []
                if len(new_word) > 0 and word != new_word:
                    if x < len(ls) - 1 and ls[x+1] == '"':
                        word1 = word[:-1]
                        word2 = word[-1]
                        new_list.append(word1)
                        new_list.append(word2)
                else:
                    new_list.append(word)
                for new_word_list in new_list:
                    if new_word_list in unknown_list:
                        unknown_list[new_word_list] += 1
                    else:
                        unknown_list[new_word_list] = 1
                    dictionary.add(new_word_list)
                    result.append(new_word_list)
        unknown_list = {k:v for k,v in unknown_list.iteritems() if v==self.unknown_threshold}

        return (result, unknown_list, dictionary)
