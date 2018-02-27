# -*- coding: utf-8 -*-
import time
import wm_model
from send import report

connetions_list = {}

# Проверка на подключение
def check_connection():
    try:
        time_to_send = time.time() + 60
        while True:

            checking_of_vodomats(wm_model.wm_list, time.time() - 15)

            if time.time() > time_to_send:
                notification(time_to_send)
                time_to_send += 3600

            time.sleep(5)

    except KeyError as e:
        print(e)

    return False


# Проверка водоматов на связь
def checking_of_vodomats(vodomats, last_time):

    for vodomat in vodomats:
        if vodomats[vodomat]['communication'] and vodomats[vodomat]['last_time'] < last_time:
            connetions_list.update(
                {vodomat: {'what_is_the_time_lost': vodomats[vodomat]['last_time'], 'communication': False}})
            report('Связь с [%s] водоматом потеряна' % vodomat)

        elif connetions_list.get(vodomat) is not None:
            if vodomats[vodomat]['communication'] and vodomats[vodomat]['last_time'] > last_time and not \
            connetions_list[vodomat]['communication']:
                connetions_list.update(
                    {vodomat: {'what_is_the_time_get': vodomats[vodomat]['last_time'], 'communication': True}})
                report('Связь с [%s] водоматом налажена' % vodomat)


# Опевещение о состояни водомата
def notification(time_to_send):
        report(str(module.connected_vodomats().get('status')))