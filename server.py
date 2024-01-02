"""
Flask server for receiving inbound signals from Homebridge using homebridge-http-webhooks
@see https://github.com/benzman81/homebridge-http-webhooks
"""

from flask import Flask, jsonify


server = Flask(__name__)
message_queue = {}


@server.route('/screen-on', methods=['GET'])
def _screen_on():
    message_queue.put('screen-on')
    return jsonify({"status": "success"})


@server.route('/screen-off', methods=['GET'])
def _screen_off():
    message_queue.put('screen-off')
    return jsonify({"status": "success"})


def run_server(msg_queue):
    global message_queue
    message_queue = msg_queue
    print('Starting Flask')
    server.run(host='0.0.0.0', port=5500)
