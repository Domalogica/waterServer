"""
модуль основной логики
"""
from flask import jsonify, abort
import time
from app import last_save

import db_menedger
from db_menedger import connect_mysql

import billing


# запись в БД информации о сессии
def write_session(wm, raw):
    connect_mysql.insert_session(wm=wm, data=raw)


# Функция для парсига HTTP запроса
def pars_requests(request):
    return request.args.get('wm', type=int), request.get_json()

# Проверка связи с водоматом
def checking_of_connection(wm):
    return 'Ok'

# Данные от водомата для расчеов и их занесения в бд
def save_of_data(wm, data):
    return 'Updated'

# Подключение к водомату
def connect_to_wm(wm, telegram):
    return 'Ok'