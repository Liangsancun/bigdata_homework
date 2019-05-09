# coding=utf-8
import json
import pymysql

def connect_db(host, db, user, passwd, port=3306):
    # 建立数据库的连接
    conn = pymysql.connect(
        host=host,  # 要连接的主机公网地址。在本地时，host='localhost'或'127.0.0.1'。
        port=port,
        user=user,  # 用户名
        passwd=passwd,  # 密码
        db=db,  # mysql中的哪个数据库
        charset='utf8'
    )
    # 获取游标（类型设置为字典形式）
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return cur, conn

def load_data(file_path):
    arr = []
    with open(file_path,'r',encoding='utf-8') as f:
        for line in f:
            arr += json.loads(line.strip())
    return arr



def insert_to_table(cur, conn, sql, data, one_commit_num):
    '''
    :param cur:
    :param conn:
    :param data: 列表，cur.executemany(sql,data)的data的形式
    :param one_commit_num: 一次事务提交的条目数
    :return:
    '''
    a = len(data)
    b = a / one_commit_num
    c = a / one_commit_num
    # 批次提交，一次是one_commit_num个，其中最后一次提交的数据的开始下标为begin_index_num
    begin_index_num = b if a > b else b - 1

    i = 0
    while (i <= begin_index_num):
        if i == begin_index_num:
            args = data[one_commit_num * i:]
            try:
                cur.execute(sql, args)
                conn.commit()  # 事务提交
            except Exception as e:
                conn.rollback()  # 事务回滚
                print('下标%d处上传失败' % (i * one_commit_num), e)
            else:

                print('全部提交成功')
                i += 1  # 进行下一个批处理



        else:
            scale_begin = one_commit_num * i
            scale_end = one_commit_num * (i + 1)
            args = data[scale_begin:scale_end]  # eg: 1000*i~1000*i+999
            try:
                cur.executemany(sql, args)
                conn.commit()  # 事务提交
            except Exception as e:
                conn.rollback()  # 事务回滚
                print('下标%d处上传失败' % (i * one_commit_num), e)
            else:

                print('下标%d~%d提交成功' % (scale_begin, scale_end))
                i += 1  # 进行下一个批处理


if __name__ == '__main__':
	#加载数据
    hotels = load_data('hotels.txt')
    comments = load_data('comments.txt')
    near_hotels = load_data('near_hotels.txt')
    near_scenes = load_data('near_scenes.txt')
    near_eatings = load_data('near_eatings.txt')

	#连接数据库
    cur, conn = connect_db('62.234.53.229', 'hotel', 'liang', 'liang')
	#导入语句
    sql_insert = 'insert ignore into hotels values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    sql_comments_insert = 'insert ignore into comments values(%s,%s,%s,%s,%s,%s,%s,%s)'
    sql_near_hotels_insert = 'insert ignore into near_hotels values(%s,%s,%s,%s)'
    sql_near_scenes_insert = 'insert ignore into near_scenes values(%s,%s,%s,%s)'
	#事务提交导入
    insert_to_table(cur, conn, sql_insert, hotels, 300)
    insert_to_table(cur,conn,sql_comments_insert,comments,300)
    insert_to_table(cur,conn,sql_near_hotels_insert,near_hotels,5000)
    insert_to_table(cur,conn,sql_near_scenes_insert,near_scenes,1000)
    #关闭连接
    cur.close()
    conn.close()


