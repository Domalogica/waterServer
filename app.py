"""
файл с основным функционалом
здесь будет весь API для работы с внешним сервисами
"""
from flask import Flask, request, abort, jsonify
import json

import core

app = Flask(__name__)


def response_json(d):
    return json.dumps(d)


@app.route('/')
def home():
    return jsonify({'ok': True})


@app.route('/users')
def users():
    return jsonify({'ok': True})


@app.route('/connect')
def connect():
    return core.connect_to_wm(request.args.get('wm', type=int), request.args.get('telegram', type=int))


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
