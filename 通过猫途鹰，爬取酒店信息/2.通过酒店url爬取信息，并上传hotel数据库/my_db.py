#coding=utf-8
import pymysql
import json
import time 
import traceback
class DB(object):
    # DB('114.115.121.345','Movie','Movie','HLSiC',3306(缺省))
    def __init__(self,*db_args):
        """
        :param db_args: (host,database,user,passwd,port=3306)
        """
        self.host = db_args[0]
        self.database = db_args[1]
        self.user = db_args[2]
        self.passwd = db_args[3]
        if len(db_args) == 5:

            self.port = db_args[4]
        else:
            self.port = 3306

        self.cur,self.conn = self.connect_db()

    def connect_db(self):
        # 建立数据库的连接
        conn = pymysql.connect(
            host=self.host,  # 要连接的主机公网地址。在本地时，host='localhost'或'127.0.0.1'。
            port=self.port,
            user=self.user,  # 用户名
            passwd=self.passwd,  # 密码
            db=self.database,  # mysql中的哪个数据库
            charset='utf8'
        )
        # 获取游标（类型设置为字典形式）
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
        return cur, conn

    def create_tables(self,*tables):
        """
        :param tables:是不长度不固定的二维数组，
                其中每个数组形式 table_1 = ['表名','li int(2) not null, aa int(2) not null, primary key(li)']
        """
        for table in tables:
                # 构建新建表的语句
                # sql_create='create table syn(
                # syn varchar(100) not null,
                # primary key(syn)# 复合主键,
                # )default charset=utf8'

                sql_create = 'create table '+table[0]+'('+table[1]+')default charset=utf8'
                #提交
                self.cur.execute(sql_create)
                self.conn.commit()
        for table in tables:
            table_name = table[0]
            # 返回每个新建表的情况
            sql_check = 'desc '+table_name
            self.cur.execute(sql_check)
            res = self.cur.fetchall()
            for i in range(len(res)):
                a = res[i]
                print('表名：%s, 字段：%s, 类型: %s, 主键?: %s' % (table_name, a['Field'], a['Type'], a['Key']))


    def insert_to_table(self, table_name, data, one_commit_num):
        '''
        插入
        :param sql: 插入语句
        :param data: 列表，cur.executemany(sql,data)的data的形式[[],[],]
        :param one_commit_num: 一次事务提交的条目数
        '''
        # SQL插入语句中%s的个数
        columns_num = self.cur.execute('desc '+table_name)
        arr_s = []
        for i in range(columns_num):
            arr_s.append('%s')
        #  sql = 'insert ignore into xx values(%s,%s)'
        # ignore如果主键部分在表中已经存在，则不插
        sql = 'insert ignore into '+table_name+' values('+','.join(arr_s)+')'
        print(columns_num)
        print(sql)
        a = len(data)
        b = a / one_commit_num #7.8 7
        c = int(a / one_commit_num)#7==int(7.8)
        # 批次提交，一次是one_commit_num个，其中最后一次提交的数据的开始下标为begin_index_num
        begin_index_num = c if b > c else c-1 #之所以c为基，因为c是整数

        i = 0 # 提交的数据块的下标
        while (i <= begin_index_num):
            if i == begin_index_num:
                scale_begin = one_commit_num * i
                args = data[scale_begin:]
                if len(args) == 1:#当args中只有一个时，eg，[[1,2]]，它会认为[1,2]是一个参数，导致参数不等于2，报错
                    args = args[0] #使得[1,2] 参数个数为2，也可以变成[[1,2],]
                    #执行插入一条
                    try:
                        self.cur.execute(sql, args)
                        self.conn.commit()  # 事务提交
                    except Exception as e:
                        self.conn.rollback()  # 事务回滚
                        traceback.print_exc()
                        print('下标%d处上传失败' % (i * one_commit_num), args)
                    else:
                        print('下标%d~%d提交成功' % (scale_begin, a-1)) #a=len(data)
                        print('提交成功,共%d' % (a))
                        i += 1  # 进行下一个批处
                else: #执行插多条
                    try:
                        self.cur.executemany(sql, args)
                        self.conn.commit()  # 事务提交
                    except Exception as e:
                        self.conn.rollback()  # 事务回滚
                        traceback.print_exc()
                        print('下标%d处上传失败' % (i * one_commit_num), args)
                    else:
                        print('下标%d~%d提交成功' % (scale_begin, a - 1))  # a=len(data)
                        print('提交成功,共%d' % (len(data)))
                        i += 1  # 进行下一个批处理
            else:
                scale_begin = one_commit_num * i
                scale_end = one_commit_num * (i + 1)
                args = data[scale_begin:scale_end]  # eg: 1000*i~1000*i+999
                try:
                    self.cur.executemany(sql, args)
                    self.conn.commit()  # 事务提交
                except Exception as e:
                    conn.rollback()  # 事务回滚
                    traceback.print_exc()
                    print('下标%d处上传失败' % (i * one_commit_num), args)
                else:

                    print('下标%d~%d提交成功' % (scale_begin, scale_end-1))
                    i += 1  # 进行下一个批处理

    def close(self):
        self.cur.close()
        self.conn.close()
if __name__ == '__main__':
    #使用方法
    #连接数据库 host,database名，user名，密码
    db = DB('62.234.53.229', 'hotel', 'liang', 'liang')
    # 建的表的信息['表名’,'字段']
    # table_1 = ['ll','li int(2) not null, aa int(2) not null, primary key(li)']
    # table_2 = ['aa','li int(2) not null, aa int(2) not null, primary key(li)']
    #建表
    # db.create_tables(table_1,table_2)

    data=[[77,8],[9,10],[1,2],[4,5]]
    # 插入 '表名',data二维数组（每一个是一条，当只有一条时，用[[],]或一维数组[]），一次性提交插多少个
    db.insert_to_table('ll',data,2)
    db.close()

