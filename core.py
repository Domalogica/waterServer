"""
модуль основной логики
"""
from flask import jsonify, abort

from db_menedger import connect_mysql


# функция заглушка
def wm_task(*args):
    return args


# Подключение к водомау
def connect_to_wm(wm, user):
    user_status = False
    wm_status = False
    if user_status and wm_status:
        user_score = user
        return wm_task(wm, user_score)


# запись в БД информации о сессии
def write_session(wm, raw):
    connect_mysql.insert_session(wm=wm, data=raw)


# Функция для парсига HTTP запроса
def pars_requests(request):
    return request.args.get('wm', type=int), request.get_json()
