"""
файл с основным функционалом
здесь будет весь API для работы с внешним сервисами
"""
from flask import Flask, request, abort, jsonify
import json, threading, checking_communication

import core

app = Flask(__name__)

t = threading.Thread(target=checking_communication.check_connection)
t.start()

@app.route('/users')
def users():
    return jsonify({'ok': True})

# Обработчик для запросов по подключению к водомату
@app.route('/app/connect/wm')
def connect():
    wm = request.args.get('wm', type=int)
    user = request.args.get('user', type=int)
    return core.connect_to_wm(wm, user)

# Обработчик для запросов по отключению от водомата
@app.route('/app/disconnect/wm')
def disconnect():
    user = request.args.get('user', type=int)
    return core.disconnect_from_wm(user)

# Обработчик для проверки связи
@app.route('/wm/checking_of_communication', methods=['POST'])
def communication():

    # wm = request.args.get('wm', type=int)
    wm = request.json.get('wm')
    return json.dumps(core.checking_of_communication(wm))


# Обработчик для фиксаций изменений
@app.route('/wm/changes')
def changes_of_wm():
    wm = request.args.get('wm', type=int)
    data = request.args.get('data', type=dict)
    return core.write_changes(wm, data)

# Обработчик для фиксаций изменений
@app.route('/wm/answer')
def answer():
    wm = request.args.get('wm', type=int)
    data = request.args.get('data', type=dict)
    return core.parsing_of_answer(wm, data)


#  Прием новой сессии продаж
@app.route('/add/session', methods=['POST'])
def add_session():
    wm, raw = core.pars_requests(request)
    core.write_session(wm, raw)
    return 'ok'


app.run(host='0.0.0.0', port=8485, debug=True)
