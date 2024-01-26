"""
Flask server for receiving inbound signals from Homebridge using homebridge-http-webhooks. 
Only needed if you're going to be using Homekit
"""

import logging
from flask import Flask, jsonify

SCREEN_ON_URL = 'on'
SCREEN_OFF_URL = 'off'


server = Flask(__name__)
message_queue = {}


@server.route(f'/{SCREEN_ON_URL}', methods=['GET'])
def _screen_on():
    """ Triggers a screen on event to the clock """
    logging.info("Received screen on request")
    message_queue.put(SCREEN_ON_URL)
    return jsonify({"status": "success"})


@server.route(f'/{SCREEN_OFF_URL}', methods=['GET'])
def _screen_off():
    """ Triggers a screen off event to the clock """
    logging.info("Received screen off request")
    message_queue.put(SCREEN_OFF_URL)
    return jsonify({"status": "success"})


@server.route('/ping', methods=['GET'])
def _ping():
    """ Return true to indicate server is running """
    return "True"


def run_server(msg_queue):
    global message_queue
    message_queue = msg_queue
    logging.info('Starting Flask!')
    server.run(host='0.0.0.0', port=5500)
