# from const_list import *
from domain_of_db import connect_mysql
import datetime

list_of_users = connect_mysql.select_users()
print(list_of_users)

user_list = {1: {'balance': 10, 'current_connect': 0}}

for user in list_of_users:
    user_list.update({user['user']: user})

print('Users -> %s' % user_list)
#
# for user in list_of_users:
#     wm_list.update({wm['wm']:{'communication': False, 'full_tank': False, 'busy': False, 'task': LINKED, 'next_task': LINKED,
#                'by_till': 0, 'user': 0, 'last_time': wm['last_time'], 'up_time': 0, 'street': wm['street']}})
#


# Проверка состояния пользователя
def checking_of_user(user):
    return user_list[user]['current_connect'] == 0


# Функция для получения id водомата, к которому пользователь подключен
def current_connect(user):
    return user_list[user]['current_connect']


# Проверка состояния пользователя
def score_of_user(user):
    return user_list[user]['balance']


# Установка состояния водомата и пользователя
def set_state(user, wm):
    user_list[user].update({'current_connect': wm})
