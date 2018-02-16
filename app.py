"""
файл с основным функционалом
здесь будет весь API для работы с внешним сервисами
"""
from flask import Flask, request, abort, jsonify
import json, logging

import core

app = Flask(__name__)



logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'mylog.log')
logging.info(u'Запуск сервера')

def response_json(d):
    return json.dumps(d)


@app.route('/')
def home():
    return jsonify({'ok': True})


@app.route('/users')
def users():
    return jsonify({'ok': True})


@app.route('/connect/wm')
def connect():
    wm = request.args.get('wm', type=int)
    user = request.args.get('user', type=int)
    return core.connect_to_wm(request.args.get('wm', type=int), request.args.get('telegram', type=int))


@app.route('/wm/checking_of_connection')
def checking_of_connection():
    wm = request.args.get('wm', type=int)
    return core.checking_of_connection(wm)

@app.route('/wm/save_of_data')
def save_of_data():
    wm = request.args.get('wm', type=int)
    data = request.args.get('data', type=dict)
    return core.save_of_data(wm, data)



# Метод для запроса состаяния о водомате
@app.route('/gateway')
def gateway_get_handler():
    return core.wm_pull_config(request.args.get('wm', type=int))


@app.route('/gateway/notUpdate', methods=['POST'])
def connection():
    return jsonify({'ok': True})


# Прием новой сессии продаж
@app.route('/gateway/update/session', methods=['POST'])
def add_session():
    wm, raw = core.pars_requests(request)
    core.write_session(wm, raw)
    return 'ok'




# @app.route('/gateway/update/<method>', methods=['POST'])
# def update_wm(method):
#     core.update_wm(method, request.args.get('wm', type=int), request.get_json())
#     return core.wm_new_date(request.args.get('wm', type=int), request.get_json())
#
#
# @app.route('/gateway/<method>', methods=['POST'])
# def gateway_post_handler(method):
#     if method == 'push':
#         return core.wm_push_config(request.args.get('wm', type=int), request.get_json())
#     return abort(400)


app.run(host='0.0.0.0', port=8485, debug=True)
