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

class MysqlPython(object):

    __instance   = None
    __host       = None
    __user       = None
    __password   = None
    __database   = None
    __session    = None
    __connection = None

    def __init__(self, host='localhost', user='root', password='', database='', charset='utf8'):
        self.__host     = host
        self.__user     = user
        self.__password = password
        self.__database = database


    def _open(self):
        try:
            cnx = pymysql.connect(self.__host, self.__user, self.__password, self.__database)
            self.__connection = cnx
            self.__session    = cnx.cursor()
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0],e.args[1]))

    def _close(self):
        self.__session.close()
        self.__connection.close()

    def _one(self, query, args):

        self.__open()
        self.__session.execute(query)

        try:
            result = [item for item in self.__session.fetchone()]
            result = dict(zip(args, result))
        except:
            result = []

        self.__close()

        return result

    def _all(self, query, args):

        self.__open()
        self.__session.execute(query)

        result = []
        try:
            row = [item for item in self.__session.fetchall()]
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
            self.__session.execute(query, values)
            self.__connection.commit()

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