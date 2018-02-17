"""
модуль основной логики
"""
import time

import user_model
import wm_model
from const_list import *


def next_response(wm, up_time, raw):
    wm_model.up_time(wm, up_time)
    wm_model.linked(wm)
    return {'task': wm_model.get_task(wm)}


# Подключение к водомау
def connect_to_wm(wm, user):
    user_status = user_model.check_connecting(user)
    wm_status = wm_model.status(wm)
    if user_status:
        if wm_status == SUCCESSFUL or NOT_WATER:
            wm_model.set_task(wm, CONNECT_WM_USER, user_model.score_of_user(user))
        return wm_status
    else:
        return USER_BUSY


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