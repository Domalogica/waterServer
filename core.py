"""
модуль основной логики
"""
import user_model
import wm_model
from const_list import *


def next_response(wm, up_time, raw):
    wm_model.up_time(wm, up_time)
    wm_model.linked(wm)
    return {'task': wm_model.get_task(wm)}


# Подключение к водомау
def connect_to_wm(wm, user):

    user_status = user_model.checking_of_user(user)
    wm_status = wm_model.checking_status_of_wm(wm)

    if user_status:
        if wm_status == SUCCESSFUL or NOT_WATER:
            wm_model.set_task(wm, CONNECT_WM_USER, user_model.score_of_user(user))
        return wm_status
    else:
        return USER_BUSY



# Функция для отключения от водомата
def disconnect_from_wm(user):

    user_status = user_model.checking_of_user(user)

    if not user_status:

        wm = user_model.current_connect(user)
        wm_status = wm_model.checking_status_of_wm(wm)

        if wm_status == WM_BUSY:

            wm_model.set_task(wm, DISCONNECT_FROM_WM)

            # user_model.set_state(user, wm, True)

            return DISCONNECT_FROM_WM
        return wm_status

    else:
        return USER_BUSY




# Функция для парсига HTTP запроса
def pars_requests(request):
    return request.args.get('wm', type=int), request.get_json()


# Проверка связи с водоматом
def checking_of_communication(wm):
    wm_model.linked(wm)
    return wm_model.get_task(wm)


# Данные от водомата для расчеов и их занесения в бд
def write_changes(wm, data):

    return 'Updated'

# Разбор ответа на отключение
def parsing_of_answer(wm, data):
    user_model.set_state(wm_model.wm_list[wm].get('user'), wm, False)
    wm_model.account_settlement(wm, data)
    return

def write_session(wm, raw):
    return