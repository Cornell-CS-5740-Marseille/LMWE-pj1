class preprocessor:
    def __init__(self, file):
        with open(file) as f:
            self.data = self.data_processor(f)

    def data_processor(fhandle):
        ls = list()
        result = list()

        for line in fhandle:
            line_new = line.replace('’','\'')
            line_new = line_new.replace('``','\"')
            line_new = line_new.replace('\'\'','\"')
            line_new = line_new.replace('\' ','\'')
            line_new = line_new.replace('”','\"')
            line_new = line_new.replace('“','\"')
            ls = line_new.split()
            ls[0] = ls[0].capitalize()
            for i in range(len(ls)-1):
                if ls[i] == '.':
                    ls[i+1] = ls[i+1].capitalize()
            line_new = ' '.join(ls) + '\n'
            line_new = line_new.replace(' i ',' I ')
            ls = line_new.split()
            result.append(ls)
        return (result)

    def get_prepocessing_data(self):
        return self.data
