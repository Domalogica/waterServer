"""
модуль основной логики
"""
import user_model
import wm_model
from const_list import *
from domain_of_db import connect_mysql

def successful(wm, user, what):
    wm_model.wm_busy(wm, what=='connect')

    if what == 'connect':
        user_model.set_state(user, wm)
    else:
        user_model.set_state(user, 0)


def next_response(wm, up_time, raw):
    wm_model.up_time(wm, up_time)
    wm_model.linked(wm)
    return {'task': wm_model.get_task(wm)}


# Подключение к водомау
def connect_to_wm(wm, user):
    user_status = user_model.checking_of_user(user)
    wm_status = wm_model.status_wm(wm)

    if user_status:
        if wm_status == SUCCESSFUL or NOT_WATER:
            wm_model.set_task(wm, CONNECT_TO_WM, user_model.score_of_user(user))
        return {'return': wm_status}
    else:
        return {'return': USER_BUSY}


# Функция для отключения от водомата
def disconnect_from_wm(user):
    user_status = user_model.checking_of_user(user)
    wm = user_model.current_connect(user)
    if user_status:
        return {'return': USER_NOT_BUSY}
    else:
        wm_model.set_task(wm, DISCONNECT_FROM_WM, user)
        user_model.set_state(user, False)
        return {'return': DISCONNECT_FROM_WM}


# Функция для парсига HTTP запроса
def pars_requests(request):
    return request.args.get('wm', type=int), request.get_json()


# Проверка связи с водоматом
def communication(wm):
    wm_model.linked(wm)
    return {'task': wm_model.get_task(wm)}


# Данные от водомата для расчеов и их занесения в бд
def write_changes(wm, data):
    return 'Updated'


# Разбор ответа на отключение
def parsing_of_answer(wm, data):
    user_model.set_state(wm_model.wm_list[wm].get('user'), wm, False)
    wm_model.account_settlement(wm, data)
    return


def user_info():
    return user_model.user_list


def wm_info():
    return wm_model.wm_list

def write_session(wm, raw):
    connect_mysql.insert_session(wm, sum, **raw)