# encoding=utf-8
import pymysql
import jieba.posseg as pseg


def connect_db(host, db, user, passwd, port):
    # 建立数据库的连接
    conn = pymysql.connect(
        host=host,  # 要连接的主机地址。在本地时，host='localhost'或'127.0.0.1'。
        port=port,
        user=user,  # 用户名
        passwd=passwd,  # 密码
        db=db,  # mysql中的哪个数据库
        charset='utf8'
    )
    # 获取游标（类型设置为字典形式）
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return cur, conn


def get_db_info(cur, s):
    '''
    查看数据库中信息
    param: 数据库指针，查询语句
    return : 查询结果
    '''

    cur.execute(s)
    res = cur.fetchall()
    return res


def load_stopwords(file_path):
    '''
    加载停用词表
    param: 停用词表文件路径
    return：停用词列表
    '''
    stop_words = []
    # encoding='utf-8'时，第一个字之前会出现'\ufeff'
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            # 去掉停用词两边的\r和各种空格
            stop_words.append(line.strip())

    return stop_words


def deal_db_info(res, stop_words):
    '''
    处理从数据库中获取的信息
    param: res 从db获取的信息
           stop_words 停用词列表
    return：final 处理后的信息 是一个字符串，每个电影信息之间用\r隔开
            每个电影信息最终的加工形式为：电影名aabbccdd电影年份aabbccdd（电影名的分词+电影类型+导演们+演员们混合，每个item之间以&spark隔开）
            eg: 战狼2aabbccdd2017aabbccdd战狼&spark动作&spark战争&spark吴京&sparkJacky Wu&spark弗兰克·吉里洛&sparkFrank Grillo&spark吴刚&sparkGang Wu&spark卢靖姍&sparkCelina Jade

    '''
    final = ''  # 最终的处理结果
    length = len(res)  # 总电影数目
    flag = 1  # 标识处理到第几个电影了

    for one in res:
        # 进度条
        print("\r %d:%d" % (flag, length), end="")
        # 电影名 '青禾男高（2017）'->'青禾男高'
        movie_name = one['title'].split('（')[0].strip()

        # 电影上映时间
        movie_year = one['year']

        # 电影类型
        type_arr = one['type'].split('|')
        if len(type_arr) == 1 and type_arr[0] == '':
            type_arr = []

        # 对导演们进行处理
        directors = one['director']
        # 导演数组
        temp_arr = []
        if directors == '未知':
            director_arr = []
        else:
            # 将导演们的名字分别取出
            directors_arr = directors.split('|')
            # 导演名字有两种形式。一种:pat cruz，另一种:帕特·柯如思 pat cruz，对其进行.split(' ')，若长度为2，则是一个人的名字
            # 否则是按两个名字处理
            for i in directors_arr:
                temp = i.strip().split(' ')  # 有的名字前有空格，故.strip()
                if len(temp) == 3:
                    temp_arr.append(temp[0])
                    temp_arr.append(temp[1] + ' ' + temp[2])

                else:
                    temp_arr.append(i.strip())

        # 对演员们进行处理
        actors = one['actor']
        # 演员数组
        temp_ = []
        if actors == '':
            temp_ = []
        else:
            actors_arr = actors.split('|')
            for i in actors_arr:
                temp = i.strip().split(' ')
                if len(temp) == 3:
                    temp_.append(temp[0])
                    temp_.append(temp[1] + ' ' + temp[2])
                else:
                    # 去掉' Rüdiger Klink'的空格
                    temp_.append(i.strip())

        # 对电影名进行分词，只保留名词和动词，同时去掉停用词
        name_seg = pseg.cut(movie_name)
        name_seg_list = []
        for word, tag in name_seg:
            if word not in stop_words and word != '\r':
                if 'v' in tag or 'n' in tag:
                    name_seg_list.append(word)

        # 电影名分词+类型数组+导演数组+演员数组
        t_d_a_s = name_seg_list + type_arr + temp_arr + temp_
        # 对一个电影信息最终的处理结果
        one_line = movie_name + 'aabbccdd' + movie_year + 'aabbccdd' + '&spark'.join(t_d_a_s)

        # 加上'\n'，使一个电影的信息是一行
        final += one_line + '\n'
        flag += 1

    return final


if __name__ == '__main__':
    print('连接数据库..')
    # 连接数据库
    cur, conn = connect_db('114.115.151.219', 'Moviedb', 'Moviedb', 'HLSi7rbCpWTAbZFC', 3306)
    print('连接数据库成功，正在从数据库获取信息..')
    # 从数据库获取电影名，上映年份，类型，导演，演员信息,简介
    res = get_db_info(cur, 'select title,year,type,director,actor,summary from imdb_info2')
    print('从数据库获取数据成功')
    cur.close()
    conn.close()


    # 加载停用词表
    stop_words = load_stopwords(r'I:\python小技巧\stopwords.txt')
    print('加载停用词表成功')
    print('处理电影数据..')
    # 处理从数据库获取的信息
    txt = deal_db_info(res, stop_words)

    # 保存最后的信息
    with open('movie_seg.txt', 'w', encoding='utf-8') as f:
        f.write(txt)
    print('保存信息成功')