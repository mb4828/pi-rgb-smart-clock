"""
Mini Flask server for receiving inbound signals from Homebridge
"""

from flask import Flask, jsonify

server = Flask(__name__ + "-flask")


@server.route('/on', methods=['GET'])
def _on():
    print('ON SIGNAL RECEIVED')
    return jsonify({"status": "success"})


@server.route('/off', methods=['GET'])
def _off():
    print('OFF SIGNAL RECEIVED')
    return jsonify({"status": "success"})


def run_server():
    print('Starting Flask')
    server.run(host='0.0.0.0', port=5500)
