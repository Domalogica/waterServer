"""
модуль основной логики
"""
import user_model
import wm_model
from const_list import *
from domain_of_db import connect_mysql


def successful(wm, user, what):
    wm_model.wm_busy(wm, what == 'connect')
    if what == 'connect':
        user_model.set_state(user, wm)
    else:
        user_model.set_state(user, 0)


def next_response(wm, up_time, raw):
    wm_model.up_time(wm, up_time)
    wm_model.linked(wm)
    return {'task': wm_model.get_task(wm)}


# Добавить нового пользователя
def adding_of_user(data):

    # if connect_mysql.select_user(data['user']) == []:

    if user_model.user_list.get(data['user']) is None:

        # connect_mysql.insert_user(**data)
        user_model.user_list.update({data['user']: data})
        return USER_ADDED
    else:
        return USER_ALREADY_EXIST


# Проверка состояния пользователя
def check(user):
    try:
        user_status = user_model.checking_of_user(user)
    except KeyError:
        return NOT_SUCH_USER
    return user_status


# Подключение к водомау
def connect_to_wm(wm, user):

    user_status = check(user)

    wm_status = wm_model.status_wm(wm)

    if user_model == NOT_SUCH_USER:
        return {'return': user_status}
    elif user_status:
        if wm_status == SUCCESSFUL or NOT_WATER:
            wm_model.set_task(wm, CONNECT_TO_WM, user_model.score_of_user(user), user)
        return {'return': wm_status}
    else:
        return {'return': USER_BUSY}


# Функция для отключения от водомата
def disconnect_from_wm(user):

    user_status = check(user)

    wm = user_model.current_connect(user)

    if user_model == NOT_SUCH_USER:
        return {'return': user_status}
    elif user_status:
        return {'return': USER_NOT_BUSY}
    else:
        wm_model.set_task(wm, DISCONNECT_FROM_WM, user=user)
        # user_model.set_state(user, 0)
        return {'return': DISCONNECT_FROM_WM}


# Функция для парсига HTTP запроса
def pars_requests(request):
    return request.args.get('wm', type=int), request.get_json()


# Проверка связи с водоматом
def communication(wm):
    wm_model.linked(wm)
    return {'task': wm_model.get_task(wm)}



def user_info():
    return user_model.user_list


def wm_info():
    return wm_model.wm_list


def write_session(wm, sum_sale, raw):
    connect_mysql.insert_session(wm, sum_sale, **raw)


# Функция для добавления событий(изменений который зачастуют в водомате)
def add_event(wm, raw):
    # в дб
    return connect_mysql.insert_events(wm, **raw)


# Функция для добавления нового комментария
def add_comment(**data):
    connect_mysql.insert_comment(**data)
    return {'return': THANKS_FOR_COMMENT}


# Функция для добавления новых рекомендаций
def add_recommned(**data):
    connect_mysql.insert_recommneds(**data)
    return {'return': THANKS_FOR_RECOMMENDS}


# Функция для запроса баланса
def get_score(user):
    return user_model.user_list[user].get('balance')