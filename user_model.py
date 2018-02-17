# from const_list import *


user_list = {1: {'balance': 10, 'current_connect': 0}}


# Проверка состояния пользователя
def check_connecting(user):
    return user_list[user]['connecting'] == 0


# Проверка состояния пользователя
def score_of_user(user):
    return user_list[user]['balance']
