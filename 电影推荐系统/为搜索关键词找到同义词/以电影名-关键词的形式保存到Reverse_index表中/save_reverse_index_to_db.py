# coding=utf-8
#coding=utf-8
import json
import pymysql
def change_format(file_path):
    # 最后保存的内容：一行是一条，字段间用 '\t'隔开
    final = ''
    arr = []
    # 改变数据格式，一个关键词对应的电影名s在数据库有若干条
    with open(file_path,'r',encoding='utf-8') as f:
        for line in f:
            arr.append(line.strip())


    length = len(arr)
    flag = 1
    for line in arr:
        print('\r %d:%d' % (flag, length), end='')
        a = line.split('\t')
        keyword = a[0]
        movie_names = a[1].split('&spark&')[:-1]  # 最后一个是''

        for name in movie_names:
            one_line = keyword + '\t' + name
            final += one_line + '\n'
        flag += 1

    # 保存
    with open('reverse_index_db_format.txt','w',encoding='utf-8') as f:
        f.write(final)

    print('修改数据格式，并保存到reverse_index_db_format.txt成功')

def connect_db(host,db,user,passwd,port=3306):
    # 建立数据库的连接
    conn = pymysql.connect(
    	host=host,#要连接的主机地址。在本地时，host='localhost'或'127.0.0.1'。
        port=port,
        user=user,#用户名
        passwd=passwd, #密码
        db=db, #mysql中的哪个数据库
        charset='utf8'
    )
    # 获取游标（返回类型设置为字典形式[{},{}]，默认是元组((),())）
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return cur,conn


def load_data(file_path):
    '''
    :param file_path:
    :return: [['keyword1','syns1],['keyword2','syns2],]
    '''
    data = []
    with open(file_path,'r',encoding='utf-8') as f:
        for line in f:
            a = line.strip().split('\t')
            if len(a) == 2:
                data.append([a[0],a[1]])
    return data

def insert_to_reverse_index(cur,conn,sql,data,one_commit_num):
    '''
    :param cur:
    :param conn:
    :param data:
    :param one_commit_num: 一次事务提交的条目数
    :return:
    '''
    a = len(data)
    b = a/one_commit_num
    c = a/one_commit_num
    # 批次提交，一次是one_commit_num个，其中最后一次提交的数据的开始下标为begin_index_num
    begin_index_num = b if a>b else b-1

    i = 0
    while(i <= begin_index_num):
        if i == begin_index_num:
            args = data[one_commit_num*i:]
            try:
                cur.execute(sql,args)
            except Exception as e:
                conn.rollback() #事务回滚
                print('下标%d处上传失败'%(i*one_commit_num),e)
            else:
                conn.commit() #事务提交
                print('全部提交成功')
                i += 1 # 进行下一个批处理



        else:
            scale_begin = one_commit_num*i
            scale_end = one_commit_num*(i+1)
            args = data[scale_begin:scale_end] # eg: 1000*i~1000*i+999
            try:
                cur.executemany(sql,args)
            except Exception as e:
                conn.rollback() #事务回滚
                print('下标%d处上传失败'%(i*one_commit_num),e)
            else:
                conn.commit() #事务提交
                print('下标%d~%d提交成功'%(scale_begin,scale_end))
                i += 1 # 进行下一个批处理




if __name__ == '__main__':

    file_path_raw_data = r'../关键词电影倒排索引的文件/part-00000'
    #加载要存到数据库的数据，修改格式，并保存
    # change_format(file_path_raw_data)
    # 连接数据库
    cur, conn = connect_db('111.231.253.217', 'movie', 'movie', 'zDwMyDKLEzYeJnif', 3306)

    file_path_data = r'./reverse_index_db_format.txt'
    # 加载数据
    data = load_data(file_path_data)
    print('加载数据成功')
    print(len(data))

    # mysql插入语句
    sql_insert = 'insert ignore into reverse_index(key_word,movie_name) values(%s,%s)'
    # 插入数据
    insert_to_reverse_index(cur,conn,sql_insert,data,5000)

    cur.close()
    conn.close()







