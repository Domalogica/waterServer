"""
файл с основным функционалом
здесь будет весь API для работы с внешним сервисами
"""
from flask import Flask, request, abort, jsonify
import json, logging

import core

app = Flask(__name__)

last_save = {}


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
    return core.connect_to_wm(wm, user)


# Метод для запроса состаяния о водомате
@app.route('/gateway')
def gateway_get_handler():
    return core.wm_pull_config(request.args.get('wm', type=int))


@app.route('/gateway/notUpdate', methods=['POST'])
def connection():
    wm = request.args.get('wm', type=int)
    up_time = request.args["up_time"]
    raw = request.get_json()
    return jsonify(core.next_response(wm, up_time, raw))


# Прием новой сессии продаж
@app.route('/gateway/update/session', methods=['POST'])
def add_session():
    wm, raw = core.pars_requests(request)
    core.write_session(wm, raw)
    return 'ok'


app.run(host='0.0.0.0', port=8485, debug=True)
