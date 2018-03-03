# #!/usr/bin/python
# # -*- coding: utf-8 -*-
# import pymysql.cursors
# import time
#
#
#
# def connect():
#     connection = pymysql.connect(host='127.0.0.1',
#                                  user='root',
#                                  password='7087',
#                                  db='vodomat',
#                                  charset='utf8mb4',
#                                  cursorclass=pymysql.cursors.DictCursor)
#     return connection
#
#
# def open_db(first, second):
#
#     connection = connect()
#     cursor = connection.cursor()
#
#     cursor.execute(first, second)
#     connection.commit()
#     cursor.close()
#     connection.close()
#
#     return True
#
# def add_host(idv): # Add a new Vodomat
#
#   first = "INSERT INTO vs (idv, State, input10Counter, out10Counter, milLitlose, milLitWentOut, milLitContIn, waterPrice, contVolume, totalPaid, sessionPaid, leftFromPaid, container, currentContainerVolume, consumerPump, mainPump, magistralPressure, mainValve, filterValve, washFilValve, tumperMoney, tumperDoor, serviceButton, freeButton, Voltage, cashing, credit, sale, containerMinVolume, billAccept, maxContainerVolume, stateGraph, containerGraph) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#   second = ()
#
#   open_db(first, second)
#
#   return True
#



#!/usr/bin/env python
# coding=utf-8

import pymysql

    __instance = None
    __host = None
    __user = None
    __password = None
    __database = None
    __session = None
    __connection = None

    def __init__(self, host='localhost', user='root', password='', database='', charset='utf8'):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

    def _open(self):
        try:
            cnx = pymysql.connect(self.__host, self.__user, self.__password, self.__database)
            self.__connection = cnx
            self.__session = cnx.cursor()
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))

    def _close(self):
        self.__session.close()
        self.__connection.close()

    def _one(self, query, args):

        self._open()
        self.__session.execute(query)

        try:
            result = [item for item in self.__session.fetchone()]
            result = dict(zip(args, result))
        except:
            result = []

        self._close()

        return result

    def _all(self, query, args):

        self._open()
        self.__session.execute(query)

        result = []
        try:
            row = [item for item in self.__session.fetchall()]
            for res in row:
                result.append(dict(zip(args, res)))
        except:
            result = []

        self._close()

        return result

    # Добавить запись в БД
    def _insert(self, table, param):

        query = "INSERT INTO %s " % table

        self._open()

        keys = param.keys()
        values = tuple(param.values())

        query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + ") VALUES (" + ",".join(
            ["%s"] * len(values)) + ")"

        try:
            self.__session.execute(query, values)
            self.__connection.commit()

        except Exception as e:
            print(e)

        self._close()

        return True

    # Функция для постройки запроса
    def _select(self, table, where, *args):

        query = 'SELECT '

        l = len(args) - 1
        for i, key in enumerate(args):
            query += "`" + key + "`"
            if i < l:
                query += ","

        if where:
            query += " WHERE %s" % where

        query += 'FROM %s' % table

        return query


    # Функционал для занесения информации о продаже
    def insert_session(self, wm, sum, **param):

        param.update(wm=wm, sum=sum)

        self._insert('sales', param)

        return {'session': param}

    # Функционал для занесения информации об оплате литров
    def insert_score(self, sum, type_of_session, **param):

        param.update(sum=sum, type=type_of_session)

        self._insert('im_moneys', param)

        return {'param': param}

    def insert_user(self, **data):
        return self._insert('users', data)


    # Функционал для занесения отзыва
    def insert_comment(self, **param):
        return self._insert('reviews', param)


    # Функционал для занесения рекомендаций
    def insert_recommneds(self, **param):
        return self._insert('recommends', param)


    # Функционал для занесения событий в водомате
    def insert_events(self, wm, **param):

        param.update(wm=wm)

        self._insert('loging', param)

        return {'event': param}


    # Функция для запроса состояния водомата
    def select_status_of_wm(self, wm):

        args = ['state', 'totalPaid', 'leftFromPaid']

        where = "where wm = %s" % wm

        query = self._select('wm', where, *args)

        return self._one(query, *args)

    # Функция для запроса статистики по выборочным срокам
    def select_statistic(self, table, f_r_o_m, to, *args):

        where = "updated >= \'%s\' and updated < \'%s\'" % (f_r_o_m, to)

        query = self._select(table, where, *args)

        return self._all(query, *args)

    # Функция для запроса информации активности водомата
    def select_action_of_wm(self, wm):

        where = "where wm = %s" % wm

        query = 'SELECT FROM *'

        args = ['action']

        query = self._select(query, where, *args)

        return self._one(query, *args)

    # Функционал для запроса списка водоматов
    def select_wms(self):

        args = ['wm']

        query = self._select('wms', None, *args)

        print(query)

        return self._all(query, *args)

    # Функция для запроса id(проверки) пользователя
    def select_user(self, user):

        where = "where user = %s" % user

        args = ['user']

        query = self._select('users', where, *args)

        return self._one(query, *args)

    # Функция для запроса баланса пользователя
    def select_balance_of_user(self, user):

        where = "where user = %s" % user

        args = ['score']

        query = self._select('users', where, *args)

        return self._one(query, *args)


connect_mysql = MysqlPython('127.0.0.1', 'root', '7087', 'WB')



print(connect_mysql.select_wms())