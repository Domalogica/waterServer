# from const_list import *

user_list = {1: {'balance': 10, 'current_connect': 0}}


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
