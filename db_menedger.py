import time

db_wm = [{'wm': 0, 'total_paid': 0, 'water_praise': 400, 'max_volume_tank': 120000, 'last_time': 0},
         {'wm': 1, 'total_paid': 0, 'water_praise': 400, 'max_volume_tank': 120000, 'last_time': 0}]

db_usr = [{'telegram': 23, 'score': 100},
          {'telegram': 24, 'score': 100}]


def get_last_time(wm):
    return db_wm[wm]['last_time']


def get_config_wm(wm):
    try:
        return db_wm[wm]
    except IndexError:
        return {'ok': False}


def update_last_time(wm):
    db_wm[wm].update({'last_time': int(time.time())})


def set_config_wm(wm, data):
    try:
        db_wm[wm].update(data)
        return {'ok': True}
    except IndexError:
        return {'ok': False}


def get_user_score(telegram):
    return db_usr[telegram]
