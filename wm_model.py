import time

from const_list import *

wm_list = {1: {'communication': False, 'full_tank': False, 'busy': False, 'task': LINKED, 'next_task': LINKED,
               'by_till': 0, 'last_time': 0, 'up_time': 0}}

def up_time(wm, up_time=-1):
    if up_time == -1:
        return wm_list[wm]['up_time']
    else:
        wm_list[wm].update({'up_time': up_time})


# если link = true, записываем текушее время для проверки связь
# иначе просто обновляем link
def linked(wm, communication=True):

    try:
        wm_list[wm].update({'communication': communication})
    except:
        wm_list.update({wm:{'communication': communication}})

    if communication:
        wm_list[wm].update({'last_time': int(time.time())})
    print(wm_list)
    return {'last_save': 'saved'}

# получаем следующую задачу
def get_task(wm):
    wm_list[wm]['task'] = wm_list[wm]['next_task']
    wm_list[wm]['next_task'] = LINKED
    if wm_list[wm]['task'] == CONNECT_TO_WM:
        return wm_list[wm]['task'], wm_list[wm]['by_till']
    else:
        return wm_list[wm]['task']


# установка на следующую задачу
def set_task(wm, task, balance=0):
    if task == LINKED:
        wm_list[wm].update({'next_task': task})
    elif task == CONNECT_TO_WM:
        wm_list[wm].update({'next_task': task, 'by_till': balance})


# проверка статуса водомата
def checking_status_of_wm(wm):
    try:
        _wm = wm_list[wm]
    except KeyError:
        return NOT_WM

    if not _wm['communication']:
        return NOT_CONNECT_WM

    elif _wm['busy'] or _wm['next_task'] != LINKED:
        return WM_BUSY

    elif not _wm['full_tank']:
        return NOT_WATER

    else:
        return SUCCESSFUL

