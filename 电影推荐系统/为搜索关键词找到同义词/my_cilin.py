#coding=utf-8
class Get_cilin_info(object):
    def __init__(self):
        self.words_by_code = {}
        self.codes_by_word = {}
        self.read_cilin()

    def read_cilin(self):
        """
        读入同义词词林，编码为key，词群为value，保存在self.words_by_code
        单词为key，编码为value，保存在self.codes_by_word
        """
        file_path = r'F:\软微作业\研一下\大数据作业\nlp部分\CilinSimilarity-master\data\cilin.txt'
        with open(file_path, 'r', encoding='gbk') as f:
            for line in f.readlines():
                res = line.split()
                code = res[0]
                words = res[1:]
                # {'Hn05A10=':['杀敌','杀人'],}
                self.words_by_code[code] = words
                # codes_by_word {'杀敌':['jasdfa=','sdsdas*'],}
                for w in words:
                    if w in self.codes_by_word.keys():
                        self.codes_by_word[w].append(code)
                    else:
                        self.codes_by_word[w] = [code]

    def get_syns_by_word(self,word):
        if word in self.codes_by_word.keys():
            codes = self.codes_by_word[word]
            syns = []
            for code in codes:
                syns += self.words_by_code[code]

            return syns
        else:
            return []