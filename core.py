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

def get_score():
    return