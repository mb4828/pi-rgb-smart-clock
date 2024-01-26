import logging
import multiprocessing
import queue
import time

import requests

from api import TemperApi, get_all
from config import HOMEBRIDGE_IP, HOMEBRIDGE_PORT
from server import run_server

logging.basicConfig(encoding='utf-8', level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def run_clock(message_queue):
    while True:
        # check for messages
        try:
            message = message_queue.get_nowait()
            logging.debug('GOT MESSAGE: ' + message)
        except queue.Empty:
            pass  # no new messages - continue

        # get data from apis
        api_data = get_all()

        # update clock display
        logging.debug(f'{api_data.get("local_time")} | {api_data.get("local_date")}')
        if 'weather' in api_data:
            logging.debug(f'{api_data.get("weather").get("temp")}° | {api_data.get("weather").get("humidity")}%')
        if 'forecast' in api_data:
            logging.debug(api_data.get("forecast"))
        if 'stocks' in api_data:
            logging.debug(
                ' | '.join(
                    [f'{stock["name"]}: {stock["price"]} {stock["points"]} [{stock["percent"]}]'
                     for stock in api_data.get("stocks")]))
        if 'temper' in api_data:
            logging.debug(f'{api_data.get("temper").get("temp")}°')
        logging.debug('')

        time.sleep(1)


def run_temper():
    """ Sends Homebridge the temperature reading from Temper2 """
    while True:
        temp = TemperApi.fetch().get('temp')
        req = requests.get(f'http://{HOMEBRIDGE_IP}:{HOMEBRIDGE_PORT}/?accessoryId=temper2sensor&value={temp}')
        logging.info(f'Sent temperature to Homebridge and received code {req.status_code}')
        time.sleep(60)


def main():
    message_queue = multiprocessing.Queue()

    clock_proc = multiprocessing.Process(target=run_clock, args=(message_queue,))
    clock_proc.start()

    temper_proc = multiprocessing.Process(target=run_temper)
    temper_proc.start()

    try:
        run_server(message_queue)
    except KeyboardInterrupt:
        pass  # Ctrl+C to terminate Flask
    finally:
        clock_proc.terminate()
        temper_proc.terminate()
        clock_proc.join()
        temper_proc.join()


if __name__ == '__main__':
    main()
