# coding=utf-8
import re


class preprocessor:
    def __init__(self, file1, method, file2 = None):
        self.unknown_symbol = "<u>"
        self.unknown_threshold = 1
        self.start_symbol = "<s>"  # start of document
        self.end_symbol = "</s>"  # end of document
        self.method = method
        f1 = open(file1)
        if file2 != None:
            f2 = open(file2)
        else:
            f2 = None
        self.data = self.data_processor(f1,self.method,f2)
        #with open(file) as f:
        #    self.data = self.data_processor(f)

    #fhandle1 : train/test data
    #fhandle2 : 5000 frequently used words
    #method: unknown word processing: 0: 1->u or 1: 5000->u
    def data_processor(self, fhandle1, method, fhandle2 = None):
        ls = list()
        result = list()
        unknown_list = dict()
        dictionary = set()
        dic_5000 = set()
        tmp = list()
        result_line = list()
        replacement = list()
        replacement_line = list()

        if fhandle2 != None:
            for line in fhandle2:
                line_new = line.replace(' ','')
                ls = line_new.split()
                dic_5000.add(ls[0])

        for line in fhandle1:
            line_new = line.replace('’','\'')
            line_new = line_new.replace('``','\"')
            line_new = line_new.replace('\'\'','\"')
            line_new = line_new.replace('\' ','\'')
            line_new = line_new.replace('”','\"')
            line_new = line_new.replace('“','\"')
            line_new = line_new.replace('\n', ' '+self.end_symbol)
            # ls[0] = ls[0].capitalize()
            # for i in range(len(ls)-1):
            #     if ls[i] == '.':
            #         ls[i+1] = ls[i+1].capitalize()
            # line_new = ' '.join(ls) + '\n'
            # line_new = line_new.replace(' i ',' I ')
            ls = line_new.split(" ")
            tmp = []
            result.append(self.start_symbol)
            tmp.append(self.start_symbol)           #used for storing every line as a list element
            dictionary.add(self.start_symbol)
            dictionary.add(self.end_symbol)
            dictionary.add(self.unknown_symbol)
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
                if method == 0:
                    for new_word_list in new_list:
                        if new_word_list in unknown_list:
                            unknown_list[new_word_list] += 1
                        else:
                            unknown_list[new_word_list] = 1
                        dictionary.add(new_word_list)
                        result.append(new_word_list)
                        tmp.append(new_word_list)
                elif method == 1:
                    for new_word_list in new_list:
                        if new_word_list not in dic_5000 and len(new_word_list) > 2:
                            unknown_list[new_word_list] = 1
                        dictionary.add(new_word_list)
                        result.append(new_word_list)
                        tmp.append(new_word_list)
                else:
                    print("Error: Method not found")
            result_line.append(tmp)
        unknown_list = {k:v for k,v in unknown_list.iteritems() if v==self.unknown_threshold}
        replacement = map(lambda x: self.unknown_symbol if x in unknown_list else x, result)
        for i in range(len(result_line)):
            replacement_line.append(map(lambda x: self.unknown_symbol if x in unknown_list else x, result_line[i]))

        return (result, unknown_list, dictionary, replacement, result_line, replacement_line)
