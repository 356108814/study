# coding:utf-8

import pymysql

from common.decorators import fun_cost_time
from log import logger
import time


class DBMySQL(object):
    """
    数据库操作基类
    """

    def __init__(self, host, port, user, password, db):
        # TODO 连接池实现
        self._connections = []
        self._host = host
        self._port = int(port)
        self._user = user
        self._password = password
        self._db = db

        self._connection = self.create_connection()
        self._connection.autocommit(False)

    def create_connection(self):
        connection = pymysql.connect(host=self._host,
                                     port=self._port,
                                     user=self._user,
                                     password=self._password,
                                     db=self._db,
                                     autocommit=False,
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection

    @property
    def connection(self):
        return self._connection

    def query(self, sql, params_dict=None, is_fetchone=False):
        """
        执行sql查询语句。如：select * from user where name = '{name}'
        @param sql sql语句
        @param params_dict 参数字典
        @param is_fetchone 是否只返回一条记录
        @return dict列表或dict
        """
        with self.connection.cursor() as cursor:
            # sql格式化
            if params_dict:
                for (key, value) in params_dict.items():
                    sql = sql.replace('{%s}' % key, value)
            try:
                cursor.execute(sql)
            except Exception as e:
                logger.error('DBMySQL.query.sql:%s,Error:%s' % (sql, str(e)))
            if is_fetchone:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
        return result

    # @fun_cost_time
    def execute(self, sql, params_dict=None):
        """
        执行sql语句
        @param sql:
        @param params_dict:
        @return:
        """
        with self.connection.cursor() as cursor:
            # sql格式化
            if params_dict:
                for (key, value) in params_dict.items():
                    sql = sql.replace('{%s}' % key, value)
            try:
                cursor.execute(sql)
            except Exception as e:
                logger.error('DBMySQL.execute.sql:%s,Error:%s' % (sql, str(e)))
        self.connection.commit()

    def execute_sqls(self, sqls):
        """
        执行多条sql语句
        @param sqls:
        @return:
        """
        start = time.time()
        with self.connection.cursor() as cursor:
            for sql in sqls:
                try:
                    cursor.execute(sql)
                except Exception as e:
                    logger.error('DBMySQL.execute.sql:%s,Error:%s' % (sql, str(e)))
        self.connection.commit()
        print('execute_sqls:%s' % (time.time() - start))

    def executemany(self, sql, values=None):
        """
        根据值数组执行sql语句
        @param sql:
        @param values: 每条记录值dict
        @return:
        """
        with self.connection.cursor() as cursor:
            for params_dict in values:
                # sql格式化
                if params_dict:
                    for (key, value) in params_dict.items():
                        sql = sql.replace('{%s}' % key, value)
                try:
                    cursor.execute(sql)
                except Exception as e:
                    logger.error('DBMySQL.execute.sql:%s,Error:%s' % (sql, str(e)))
        self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()


if __name__ == '__main__':
    dbMySQL = DBMySQL(host='localhost', port=3306, user='root', password='root', db='aimei_data')
    sql = 'select * from t_data_aimei_user_action_201608 limit 0, 11'
    result = dbMySQL.query(sql)
    print(result)
