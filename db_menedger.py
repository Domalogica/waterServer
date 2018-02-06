"""
Модуль для работы с DB
"""

import time
import pymysql

# тестовые данные
db_wm = [{'wm': 0, 'total_paid': 0, 'water_praise': 400, 'max_volume_tank': 120000, 'last_time': 0},
         {'wm': 1, 'total_paid': 0, 'water_praise': 400, 'max_volume_tank': 120000, 'last_time': 0}]

# тестовые данные
db_usr = [{'telegram': 23, 'score': 100},
          {'telegram': 24, 'score': 100}]

class MysqlPython(object):

    _instance   = None
    _host       = None
    _user       = None
    _password   = None
    _database   = None
    _session    = None
    _connection = None

    def __init__(self, host='localhost', user='root', password='', database='', charset='utf8'):
        self.__host     = host
        self.__user     = user
        self.__password = password
        self.__database = database


    def __open(self):
        try:
            cnx = pymysql.connect(self.__host, self.__user, self.__password, self.__database)
            self._connection = cnx
            self._session    = cnx.cursor()
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0],e.args[1]))

    def __close(self):
        self._session.close()
        self._connection.close()





    def get_last_time(wm):
        return db_wm[wm]['last_time']


    def get_config_wm(wm):
        try:
            return db_wm[wm]
        except IndexError:
            return {'ok': False}


    def update_last_time(wm):
        db_wm[wm].update({'last_time': int(time.time())})


    def set_config_wm(wm, data):
        try:
            db_wm[wm].update(data)
            return {'ok': True}
        except IndexError:
            return {'ok': False}


    def get_user_score(telegram):
        return db_usr[telegram]


    def insert_session(self, wm, sum, **param):

        param.update(wm=wm, sum=sum)

        query = "INSERT INTO sales "
        keys = param.keys()
        values = tuple(param.values())
        query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + ") VALUES (" + ",".join(["%s"] * len(values)) + ")"

        self.__open(),

        self.__session.execute(query, values)
        self.__connection.commit()
        self.__close()
        # return self.__session.lastrowid

        return {'session': param}


    def insert_score(self, sum, type_of_session, **param):

        param.update(sum=sum, type=type_of_session)

        query = "INSERT INTO im_moneys "
        keys = param.keys()
        values = tuple(param.values())
        query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + ") VALUES (" + ",".join(["%s"] * len(values)) + ")"

        self.__open()

        self.__session.execute(query, values)
        self.__connection.commit()
        self.__close()
        # return self.__session.lastrowid

        return {'param': param}


connect_mysql = MysqlPython('127.0.0.1', 'root', '7087', 'WB')