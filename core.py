"""
модуль основной логики
"""
from flask import jsonify, abort
import time

import db_menedger
from db_menedger import connect_mysql

import billing


def check_connect(wm):
    return time.time() - db_menedger.get_last_time(wm) < 5


def connect_to_wm(wm, user):
    return jsonify({'ok': check_connect(wm), 'process': 'connect'})


def wm_new_date(wm, data):
    db_menedger.update_last_time(wm)
    billing.check_wm_sales(wm, data)
    return jsonify({'wm': wm, 'data': data})


def wm_pull_config(wm):
    if wm is not None:
        return jsonify(db_menedger.get_config_wm(wm))
    else:
        abort(400)


def wm_push_config(wm, data):
    result = db_menedger.set_config_wm(wm, data)
    return jsonify(result)


# запись в БД информации о сессии
def write_session(wm, raw):
    connect_mysql.insert_session(wm=wm, data=raw)


# Функция для парсига HTTP запроса
def pars_requests(request):
    return request.args.get('wm', type=int), request.get_json()
