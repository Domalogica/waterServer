import time

from domain_of_db import connect_mysql
from const_list import *

vodomats = [{'wm': 121, 'street': 'пр.Акушинского 30'},
            {'wm': 221, 'street': 'ул.Научный городок 1'},
            {'wm': 321, 'street': 'пр.Гамидова 81'},
            {'wm': 421, 'street': 'пр.А.Султана 1'},
            {'wm': 521, 'street': 'ул.Батырая 136л'},
            {'wm': 621, 'street': 'пр.Акушинского 28'},
            {'wm': 721, 'street': 'пр.Насрутдинова 107'},
            {'wm': 821, 'street': 'пр.Петра Первого 49д'},
            {'wm': 921, 'street': 'ул.Ирчи Казака 49к4'},
            {'wm': 1021, 'street': 'пр.Гамидова 49к7'},
            {'wm': 1121, 'street': 'пос. Ленинкент (центральная мечеть)'},
            {'wm': 1221, 'street': 'ул.Газопроводная 107б'},
            {'wm': 1321, 'street': 'пр.Акушинского 31'},
            {'wm': 1421, 'street': 'пр.Акушинского 11е'},
            {'wm': 1521, 'street': 'Индустриальный пр. 6в'}]

list_of_wms = connect_mysql.select_wms()

wm_list = {1: {'communication': False, 'full_tank': False, 'busy': False, 'task': LINKED, 'next_task': LINKED,
               'by_till': 0, 'user': 0, 'last_time': 0, 'up_time': 0}}

for wm in list_of_wms:
    wm_list.update({wm['wm']: wm})

print('Vodomats -> %s' % wm_list)



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
