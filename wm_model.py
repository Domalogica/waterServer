import time

from const_list import *

wm_list = {1: {'link': False, 'full_tank': False, 'not_busy': False, 'task': LINKED, 'next_task': LINKED,
               'by_till': 0, 'last_time': 0, 'up_time': 0}}


def up_time(wm, up_time=-1):
    if up_time == -1:
        return wm_list[wm]['up_time']
    else:
        wm_list[wm].update({'up_time': up_time})


# если link = true, записываем текушее время для проверки связь
# иначе просто обновляем link
def linked(wm, link=True):
    wm_list[wm].update({'link': link})
    if link:
        wm_list[wm].update({'last_time': int(time.time())})


# получаем следующую задачу
def get_task(wm):
    wm_list[wm]['task'] = wm_list[wm]['next_task']
    wm_list[wm]['next_task'] = LINKED
    if wm_list[wm]['task'] == CONNECT_WM_USER:
        return wm_list[wm]['task'], wm_list[wm]['by_till']
    else:
        return wm_list[wm]['task']


# установка на следующую задачу
def set_task(wm, task, balance=0):
    if task == LINKED:
        wm_list[wm].update({'next_task': task})
    elif task == CONNECT_WM_USER:
        wm_list[wm].update({'next_task': task, 'by_till': balance})


# проверка статуса водомата
def status(wm):
    try:
        _wm = wm_list[wm]
    except KeyError:
        return NOT_WM

    if _wm['link']:
        return NOT_CONNECT_WM
    elif _wm['not_busy'] or _wm['next_task'] != LINKED:
        return WM_BUSY
    elif _wm['full_tank']:
        return NOT_WATER
    else:
        return SUCCESSFUL

