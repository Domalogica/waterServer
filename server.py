from flask import Flask, request, abort, jsonify
import json

import api

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
    return api.connect_to_wm(request.args.get('wm', type=int), request.args.get('telegram', type=int))


@app.route('/gateway')
def gateway_get_handler():
    return api.wm_pull_config(request.args.get('wm', type=int))


@app.route('/gateway/<method>', methods=['POST'])
def gateway_post_handler(method):
    if method == 'push':
        return api.wm_push_config(request.args.get('wm', type=int), request.get_json())
    elif method == 'update':
        return api.wm_new_date(request.args.get('wm', type=int), request.get_json())

    return abort(400)


app.run(host='0.0.0.0', port=8485, debug=True)
