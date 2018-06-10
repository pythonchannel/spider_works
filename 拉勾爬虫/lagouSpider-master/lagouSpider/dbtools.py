import MySQLdb

# 导入settings设置
from scrapy.utils.project import get_project_settings


class DBTool():
    def __init__(self):
        '''读取settings中的mysql配置'''
        self.settings = get_project_settings()
        self.host = self.settings['MYSQL_HOST']
        self.port = self.settings['MYSQL_PORT']
        self.db = self.settings['MYSQL_DBNAME']
        self.user = self.settings['MYSQL_USER']
        self.pwd = self.settings['MYSQL_PASSWD']

    def conn_db(self):
        '''
        连接到 数据库
        '''
        conn = MySQLdb.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               password=self.pwd,
                               db=self.db,
                               charset='utf8mb4')
        return conn

    '''
    创建表的功能，建议直接在数据库中创建好，避免出错
    '''

    def inset_data(self, sql):
        '''
        插入数据
        :param sql:
        :param params:
        :return:
        '''
        conn = self.conn_db()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()  # 这里要commit
        except Exception as e:
            conn.rollback()  # 这里如果插入失败要回滚
            print('---出错了:' + e)
        cur.close()
        conn.close()

    def update_data(self, sql, *params):
        conn = self.conn_db()
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            conn.commit()  # 这里要commit
        except Exception as e:
            conn.rollback()  # 这里如果插入失败要回滚
            print('---出错了:' + e)
        cur.close()
        conn.close()

    def delete_data(self, sql, *params):
        conn = self.conn_db()
        cur = conn.cursor()

        cur.execute(sql, params)
        conn.commit()  # 这里要commit

        cur.close()
        conn.close()

    def query_data(self, sql):
        '''
        查询数据
        :param sql:
        :return:
        '''
        conn = self.conn_db()
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results


'''测试dbTool的类'''


class TestDBTool():
    def __init__(self):
        self.dbTool = DBTool()

    # 测试插入
    def testInsert(self):
        sql = "insert into lagou_data(`title`,`address`,`money`,`experience`,`company`,`fintance`) values('Python工程师','北京','50k','三年经验','拉勾','A轮')"
        self.dbTool.inset_data(sql)


if __name__ == "__main__":
    testdbTool = TestDBTool()
    testdbTool.testInsert()  # 执行测试插入数据

