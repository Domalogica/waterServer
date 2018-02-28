"""
файл с основным функционалом
здесь будет весь API для работы с внешним сервисами
"""
from flask import Flask, request, abort, jsonify
import json
import threading

import checking_communication
import core

app = Flask(__name__)

# t = threading.Thread(target=checking_communication.check_connection)
# t.start()


@app.route('/users')
def user_info():
    """
    Возврашает список пользвателей
    Нужен для тестов
    :return:
    """
    return jsonify(core.user_info())


@app.route('/wms')
def wm_info():
    """
    Возврашает список пользвателей
    Нужен для тестов
    :return:
    """
    return jsonify(core.wm_info())


# Обработчик для запросов по подключению к водомату
@app.route('/app/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    print(data)
    return jsonify(core.adding_of_user(data))


# Обработчик для запросов по подключению к водомату
@app.route('/app/connect/wm', methods=['POST'])
def connect():
    wm = request.args.get('wm', type=int)
    user = request.args.get('user', type=int)
    return jsonify(core.connect_to_wm(wm, user))


# Обработчик для запросов по отключению от водомата
@app.route('/app/disconnect/wm', methods=['POST'])
def disconnect():
    user = request.args.get('user', type=int)
    return jsonify(core.disconnect_from_wm(user))


@app.route('/successful/<types>', methods=['POST'])
def successful(types):
    """
    обработка сообшений о успешном подключении
    :param types: тип сообшения
        :connect = водомат подключился к пользователя
        :disconnect = водомат отключился от пользователя
    :return:
    """
    wm = request.args.get('wm', type=int)
    user = request.args.get('user', type=int)
    core.successful(wm, user, types)
    return jsonify(core.communication(wm))


# Обработчик для проверки связи
@app.route('/communication', methods=['POST'])
def communication():
    wm = request.args.get('wm', type=int)
    return jsonify(core.communication(wm))


@app.route('/developments', methods=['POST'])
def developments():
    wm, raw = core.pars_requests(request)
    return jsonify(core.add_developments(wm, raw))


#  Прием новой сессии продаж
@app.route('/add/session', methods=['POST'])
def add_session():
    wm, raw = core.pars_requests(request)
    sum_sale = request.args.get('sum', type=int)
    core.write_session(wm, sum_sale, raw)
    return jsonify(core.communication(wm))


app.run(host='0.0.0.0', port=8485, debug=True)
