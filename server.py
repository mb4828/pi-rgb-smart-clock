"""
Flask server for receiving inbound signals from Homebridge using homebridge-http-webhooks. 
Only needed if you're going to be using Homekit
"""

from flask import Flask, jsonify
from flask_crontab import Crontab
import requests

from api import TemperApi
from config import HOMEBRIDGE_IP, HOMEBRIDGE_PORT

SCREEN_ON_URL = 'on'
SCREEN_OFF_URL = 'off'


server = Flask(__name__)
crontab = Crontab(server)
message_queue = {}


@server.route(f'/{SCREEN_ON_URL}', methods=['GET'])
def _screen_on():
    """ Triggers a screen on event to the clock """
    message_queue.put(SCREEN_ON_URL)
    return jsonify({"status": "success"})


@server.route(f'/{SCREEN_OFF_URL}', methods=['GET'])
def _screen_off():
    """ Triggers a screen off event to the clock """
    message_queue.put(SCREEN_OFF_URL)
    return jsonify({"status": "success"})


@crontab.job()
def _update_temper2():
    """ Sends Homebridge the temperature reading from Temper2 every minute """
    temp = TemperApi.fetch().get('temp')
    requests.get(f'{HOMEBRIDGE_IP}:{HOMEBRIDGE_PORT}/?accessoryId=temper2sensor&value={temp}')


def run_server(msg_queue):
    global message_queue
    message_queue = msg_queue
    print('Starting Flask')
    server.run(host='0.0.0.0', port=5500)
