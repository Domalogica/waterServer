"""
Модуль для работы с DB
"""

import time, pymysql, logging

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'mylog.log')

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


    # Функционал для занесения информации о продаже
    def insert_session(self, wm, sum, **param):


        param.update(wm=wm, sum=sum)


        query = "INSERT INTO sales "
        keys = param.keys()
        values = tuple(param.values())
        query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + ") VALUES (" + ",".join(["%s"] * len(values)) + ")"

        self.__open(),

        try:
            self.__session.execute(query, values)
            self.__connection.commit()

        except Exception as e:
            logging.error(u'Fatal error %s' % e)

        self.__close()
        # return self.__session.lastrowid

        return {'session': param}

    # Функционал для занесения информации об оплате литров
    def insert_score(self, sum, type_of_session, **param):

        param.update(sum=sum, type=type_of_session)

        query = "INSERT INTO im_moneys "
        keys = param.keys()
        values = tuple(param.values())
        query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + ") VALUES (" + ",".join(["%s"] * len(values)) + ")"

        self.__open()

        try:
            self.__session.execute(query, values)
            self.__connection.commit()

        except Exception as e:
            logging.error(u'Fatal error %s' % e)

        self.__close()
        # return self.__session.lastrowid

        return {'param': param}


    # Функционал для вывода статистики по выборочным срокам
    def select_all(self, table, f_r_o_m, to, *args):

        where = "updated >= \'%s\' and updated < \'%s\'" % (f_r_o_m, to)

        result = []
        query = 'SELECT '
        keys = args
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`" + key + "`"
            if i < l:
                query += ","

        query += 'FROM %s' % table

        if where:
            query += " WHERE %s" % where

        self.__open()
        self.__session.execute(query)

        number_rows = self.__session.rowcount
        try:
            row = [item for item in self.__session.fetchall()]
            for res in row:
                result.append(dict(zip(args, res)))

        except Exception as e:
            logging.error(u'Fatal error %s' % e)
            result = []

        self.__close()

        return result

    def select_status_of_vodomat(self, wm):

        where = "where wm = %s" % wm

        result = []
        query = 'SELECT '
        keys = ['state', 'totalPaid', 'leftFromPaid']
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`" + key + "`"
            if i < l:
                query += ","

        query += 'FROM %s' % table

        if where:
            query += " WHERE %s" % where

        self.__open()
        self.__session.execute(query)

        number_rows = self.__session.rowcount
        try:
            row = [item for item in self.__session.fetchall()]
            for res in row:
                result.append(dict(zip(keys, res)))

        except Exception as e:
            logging.error(u'Fatal error %s' % e)
            result = []

        self.__close()

        return result

    def select_action_of_vodomat(self, wm):

        where = "where wm = %s" % wm

        result = []
        query = 'SELECT '
        keys = ['action']
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`" + key + "`"
            if i < l:
                query += ","

        query += 'FROM %s' % table

        if where:
            query += " WHERE %s" % where

        self.__open()
        self.__session.execute(query)

        number_rows = self.__session.rowcount
        try:
            row = [item for item in self.__session.fetchall()]
            for res in row:
                result.append(dict(zip(keys, res)))

        except Exception as e:
            logging.error(u'Fatal error %s' % e)
            result = []

        self.__close()

        return result

    # Функционал для вывода списка водоматов
    def select_all_dodomats(self):

        result = []
        query = 'SELECT '
        keys = list(['wm'])
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`" + key + "`"
            if i < l:
                query += ","

        query += 'FROM vodomats'

        self.__open()
        self.__session.execute(query)

        number_rows = self.__session.rowcount
        try:
            row = [item for item in self.__session.fetchall()]
            for res in row:
                result.append(dict(zip(keys, res)))
        except Exception as e:
            logging.error(u'Fatal error %s' % e)
            result = []

        self.__close()

        return result


    def select_user(self, telegram):

        result = []
        query = 'SELECT '

        where = "where telegram = %s" % telegram

        keys = list(['telegram'])
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`" + key + "`"
            if i < l:
                query += ","

        query += 'FROM vodomats'

        self.__open()
        self.__session.execute(query)

        number_rows = self.__session.rowcount
        try:
            row = [item for item in self.__session.fetchall()]
            for res in row:
                result.append(dict(zip(keys, res)))
        except Exception as e:
            logging.error(u'Fatal error %s' % e)
            result = []

        self.__close()

        return result

    def select_scoreof_user(self, telegram):
        result = []
        query = 'SELECT '

        where = "where telegram = %s" % telegram

        keys = list(['score'])
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`" + key + "`"
            if i < l:
                query += ","

        query += 'FROM vodomats'

        self.__open()
        self.__session.execute(query)

        number_rows = self.__session.rowcount
        try:
            row = [item for item in self.__session.fetchall()]
            for res in row:
                result.append(dict(zip(keys, res)))
        except Exception as e:
            logging.error(u'Fatal error %s' % e)
            result = []

        self.__close()

        return result


connect_mysql = MysqlPython('127.0.0.1', 'root', '7087', 'WB')