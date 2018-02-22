# -*- coding: utf-8 -*-
import time
import wm_model
from send import report

connetions_list = {}

def check_connection():
    try:
        time_to_send = time.time() + 60
        while True:
            print('ghfh')
            vodomats = wm_model.wm_list
            last_time = time.time() - 15

            for vodomat in vodomats:

                if vodomats[vodomat]['communication'] and vodomats[vodomat]['last_time'] < last_time:
                    print('%s vodomat disconnected' % vodomat)
                    connetions_list.update({vodomat: {'what_is_the_time_lost': vodomats[vodomat]['last_time'], 'communication': False}})
                    vodomats[vodomat]['communication'] = False

                    report('Связь с [%s] водоматом потеряна' % vodomat)

                elif connetions_list.get(vodomat) is not None:
                    if vodomats[vodomat]['communication'] and vodomats[vodomat]['last_time'] > last_time and not connetions_list[vodomat]['communication']:
                        vodomats[vodomat]['communication'] = True
                        connetions_list.update({vodomat: {'what_is_the_time_get': vodomats[vodomat]['last_time'], 'communication': True}})

                        print('%s vodomat connected' % vodomat)

                        report('Связь с [%s] водоматом налажена' % vodomat)

            # if time.time() > time_to_send:
            #     time_to_send += 3600
            #     report(str(module.connected_vodomats().get('status')))
            #
            time.sleep(5)

    except KeyError as e:
        # report('Fatal error %s' % e)
        print(e)

    return False