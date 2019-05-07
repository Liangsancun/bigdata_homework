#coding=utf-8
import json
import pymysql
def change_format(file_path):
    # 最后保存的内容：一行是一条，字段间用 '\t'隔开,eg: 一条 '茶馆\t茶楼'
    final = ''
    # 加载数据，并解码json
    dict_syns = {}
    with open(file_path,'r',encoding='utf-8') as f:
        dict_syns = json.loads(f.read())
    print('读取raw data成功')
    # 改变数据格式
    length = len(dict_syns)
    flag = 1
    for key,values in dict_syns.items():
        print('\r %d:%d'%(flag,length),end='')
        for value in values:

            one_line = key + '\t' + value
            final += one_line + '\n'

        flag += 1

    # 保存
    with open('movie_syns_db_format.txt','w',encoding='utf-8') as f:
        f.write(final)

    print('修改数据格式，并保存到movie_syns_db_format.txt成功')

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

def creat_table(cur,conn):
    '''
    建新表 keyword_syn
    :param cur:
    :param conn:
    :return:
    '''
    sql_create = 'create table keyword_syn(keyword varchar(100) not null,syn varchar(100) not null)'
    cur.execute(sql_create)
    conn.commit()

    # 返回新建表的情况
    cur.execute('desc keyword_syn')
    res = cur.fetchall()
    for i in range(len(res)):
        a = res[i]
        print('字段：%s 类型 %s'%(a['Field'],a['Type']))

def load_data(file_path):
    '''
    :param file_path:
    :return: [['keyword1','syns1],['keyword2','syns2],]
    '''
    data = []
    with open(file_path,'r',encoding='utf-8') as f:
        for line in f:
            a = line.strip().split('\t')
            data.append([a[0],a[1]])
    return data

def insert_to_keyword_syn(cur,conn,sql,data,one_commit_num):
    '''
    :param cur:
    :param conn:
    :param data: 列表，cur.executemany(sql,data)的data的形式
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

    file_path_raw_data = r'./获取关键字的同义词/word_syns_out.txt'
    #加载要存到数据库的数据，修改格式，并保存
    change_format(file_path_raw_data)
    # 连接数据库
    cur, conn = connect_db('111.231.253.217', 'movie', 'movie', 'zDwMyDKLEzYeJnif', 3306)
    # 建表keyword_syns
    creat_table(cur,conn)

    file_path_data = r'./movie_syns_db_format.txt'
    # 加载数据
    data = load_data(file_path_data)
    print('加载数据成功')



    # mysql插入语句
    sql_insert = 'insert into keyword_syn values(%s,%s)'
    # 插入数据
    insert_to_keyword_syn(cur,conn,sql_insert,data,5000)

    cur.execute('desc keyword_syn')
    for i in cur.fetchall():
        print('Field: %s Type: %s'%(i['Field'],i['Type']))

    res = cur.execute('select * from keyword_syn')
    print(cur.fetchmany(5))
    print('总条目数：%d'%(res))
