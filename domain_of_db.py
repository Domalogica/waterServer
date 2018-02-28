# coding=utf-8
import pymysql


class MysqlPython(object):
    _instance = None
    _host = None
    _user = None
    _password = None
    _database = None
    _session = None
    _connection = None

    def __init__(self, host='localhost', user='root', password='', database='', charset='utf8'):
        self._host = host
        self._user = user
        self._password = password
        self._database = database

    def __open(self):
        try:
            cnx = pymysql.connect(self._host, self._user, self._password, self._database)
            self._connection = cnx
            self._session = cnx.cursor()
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))

    def __close(self):
        self._session.close()
        self._connection.close()

    def __one(self, query, args):

        self.__open()
        self._session.execute(query)

        try:
            result = [item for item in self._session.fetchone()]
            result = dict(zip(args, result))
        except:
            result = []

        self.__close()

        return result

    def __all(self, query, args):

        self.__open()
        self._session.execute(query)

        result = []
        try:
            row = [item for item in self._session.fetchall()]
            for res in row:
                result.append(dict(zip(args, res)))
        except:
            result = []

        self.__close()

        return result

    # Добавить запись в БД
    def __insert(self, query, param):

        self.__open()

        keys = param.keys()
        values = tuple(param.values())

        query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + ") VALUES (" + ",".join(
            ["%s"] * len(values)) + ")"

        try:
            self._session.execute(query, values)
            self._connection.commit()

        except Exception as e:
            print(e)

        self.__close()

        return True

    # Функция для постройки запроса
    def __select(self, query, where, *args):

        l = len(args) - 1
        for i, key in enumerate(args):
            query += "`" + key + "`"
            if i < l:
                query += ","

        if where:
            query += " WHERE %s" % where

        return query

    # Функционал для занесения информации о продаже
    def insert_session(self, wm, sum, **param):

        param.update(wm=wm, sum=sum)

        query = "INSERT INTO sales "

        self.__insert(query, param)

        return {'session': param}

    # Функционал для занесения информации об оплате литров
    def insert_score(self, sum, type_of_session, **param):

        param.update(sum=sum, type=type_of_session)

        query = "INSERT INTO im_moneys "

        self.__insert(query, param)

        return {'param': param}

    # Функция для запроса состояния водомата
    def select_status_of_wm(self, wm):

        args = ['state', 'totalPaid', 'leftFromPaid']

        where = "where wm = %s" % wm

        query = 'SELECT FROM wm'

        query = self.__select(query, where, *args)

        return self.__one(query, *args)

    # Функция для запроса статистики по выборочным срокам
    def select_statistic(self, table, f_r_o_m, to, *args):

        where = "updated >= \'%s\' and updated < \'%s\'" % (f_r_o_m, to)

        query = 'SELECT FROM %s' % table

        query = self.__select(query, where, *args)

        return self.__all(query, *args)

    # Функция для запроса информации активности водомата
    def select_action_of_wm(self, wm):

        where = "where wm = %s" % wm

        query = 'SELECT FROM *'

        args = ['action']

        query = self.__select(query, where, *args)

        return self.__one(query, *args)

    # Функционал для запроса списка водоматов
    def select_wms(self):

        query = 'SELECT FROM wms'
        args = ['wm']

        query = self.__select(query, where=None, *args)

        return self.__all(query, *args)

    # Функция для запроса id(проверки) пользователя
    def select_user(self, telegram):

        query = 'SELECT FROM users'

        where = "where telegram = %s" % telegram

        args = ['telegram']

        query = self.__select(query, where, *args)

        return self.__one(query, *args)

    # Функция для запроса баланса пользователя
    def select_balance_of_user(self, telegram):

        query = 'SELECT FROM users'

        where = "where telegram = %s" % telegram

        args = ['score']

        query = self.__select(query, where, *args)

        return self.__one(query, *args)


connect_mysql = MysqlPython('127.0.0.1', 'root', '7087', 'WB')
