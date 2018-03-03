import time


from const_list import *
from domain_of_db import connect_mysql

print(connect_mysql.select_wms())

wm_list = {1: {'communication': False, 'full_tank': False, 'busy': False, 'task': LINKED, 'next_task': LINKED,
               'by_till': 0, 'user': 0, 'last_time': 0, 'up_time': 0}}


def wm_busy(wm, busy=True):
    wm_list[wm]['busy'] = busy


def up_time(wm, time_up=None):
    if time_up is None:
        return wm_list[wm]['up_time']
    else:
        wm_list[wm].update({'up_time': time_up})


# если link = true, записываем текушее время для проверки связь
# иначе просто обновляем link
def linked(wm, communication=True):
    wm_list[wm].update({'communication': communication})
    if communication:
        wm_list[wm].update({'last_time': int(time.time())})
    return SUCCESSFUL


# получаем следующую задачу
def get_task(wm):
    wm_list[wm]['task'] = wm_list[wm]['next_task']
    wm_list[wm]['next_task'] = LINKED
    if wm_list[wm]['task'] == CONNECT_TO_WM:
        return wm_list[wm]['task'], wm_list[wm]['by_till'], wm_list[wm]['user']
    else:
        return wm_list[wm]['task'],  # что бы вернуть картедж


# установка на следующую задачу
def set_task(wm, task, balance=0, user=0):
    wm_list[wm].update({'next_task': task})
    if task == CONNECT_TO_WM:
        wm_list[wm].update({'by_till': balance, 'user': user})
    elif task == DISCONNECT_FROM_WM:
        wm_list[wm].update({'user': user})


# проверка статуса водомата
def status_wm(wm):
    try:
        _wm = wm_list[wm]
    except KeyError:
        return NOT_WM

    if not _wm['communication']:
        return NOT_CONNECT_WM

    elif _wm['busy']:
        return WM_BUSY

    elif not _wm['full_tank']:
        return NOT_WATER

    else:
        return SUCCESSFUL
