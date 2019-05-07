# coding=utf-8
import synonyms as syn
import my_cilin
import json


def load_keywords(file_path):
    keywords = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            keywords.append(line.split('\t')[0])
    return keywords


def load_movie_segs(file_path):
    movie_segs = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            temp = line.strip().split('aabbccdd')
            temp2 = temp[2].split('&spark')
            movie_segs += temp[:2] + temp2

    return list(set(movie_segs))


def get_word_syns(keywords):
    a = {}
    length = len(keywords)
    flag = 1
    for keyword in keywords:
        print('\r %d:%d' % (flag, length), end='')

        syns_1 = []
        syns_2 = []

        first_char = ord(keyword[0])
        # 看是否关键词是中文，如果是英文，近义词就只有它自己，中文的话，用cilin和synonyms获取近义词
        if 64 < first_char < 123:
            pass
        else:
            # 返回[[近义词],[概率]]
            syns_1 = syn.nearby(keyword)[0]
            # 根据词林获取某词的近义词
            syns_2 = cl.get_syns_by_word(keyword)

        # 一个词通过synoym包和cilin找到的所有的近义词
        temp = list(set(syns_1 + syns_2))
        # 如果该词的某个近义词在电影分词里也出现，就保留，最终的近义词肯定有它自己
        syns = [keyword]  # 该词本身也是它自己的近义词，
        for word in temp:

            if word in movie_segs:
                syns.append(word)
        a[keyword] = list(set(syns))  # syns初始包含关键字，有的在synonyms或cilin又返回了一次该关键字，故去重

        flag += 1
    return a


if __name__ == '__main__':
    print('加载关键字..')
    # 加载关键字
    keywords_1 = load_keywords(r'../关键词电影倒排索引的文件/part-00000')
    keywords_2 = load_keywords(r'../关键词电影倒排索引的文件/part-00001')
    keywords = keywords_1 + keywords_2
    print('加载关键字成功')
    # 加载词林
    cl = my_cilin.Get_cilin_info()
    print('加载词林成功')

    # 加载电影信息里，去重后所有的分词，共有
    movie_segs = load_movie_segs(r'../../对电影信息进行分词/movie_seg.txt')
    print('加载去重后的电影分词成功')

    print('获取每个关键词在电影分词中出现的近义词..')
    # 所有词的在电影分词中存在的近义词，返回字典
    word_segs = get_word_syns(keywords)

    # 保存关键字的近义词（包括它自己）到word_syns_out.txt
    with open('word_syns_out.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(word_segs, ensure_ascii=False))
    print('已保存到word_syns_out.txt')
