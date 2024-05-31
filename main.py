import asyncio
from concurrent.futures import ProcessPoolExecutor
import os
import logging
import multiprocessing
import queue
import signal
import time

import requests

from pirgbsmartclock.api import TemperApi
from config import HOMEBRIDGE_IP, HOMEBRIDGE_PORT, TIMEZONE
from pirgbsmartclock.clock import Clock
from server import run_server

logging.basicConfig(encoding='utf-8', level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
os.environ['TZ'] = TIMEZONE
time.tzset()

try:
    os.nice(-20)  # make this process high priority to improve clock frame rate
except:
    pass


def run_clock(message_queue):
    clock = Clock()
    show_clock = True

    while True:
        # check for messages
        try:
            message = message_queue.get_nowait()
            logging.info('GOT MESSAGE: ' + message)
            show_clock = 'off' not in message
        except queue.Empty:
            pass  # no new messages - continue

        clock.run(show_clock)
        time.sleep(0.1)


def run_temper():
    """ Sends Homebridge the temperature reading from Temper2 """
    while True:
        try:
            temp = TemperApi.async_get_data().get('temp')
            req = requests.get(f'http://{HOMEBRIDGE_IP}:{HOMEBRIDGE_PORT}/?accessoryId=temper2sensor&value={temp}')
            logging.info(f'Sent temperature to Homebridge and received code {req.status_code}')
        except Exception as e:
            logging.warning(f'Failed to transmit Temper data to Homebridge: {e}')
        time.sleep(60)


def shutdown(loop):
    for task in asyncio.all_tasks(loop):
        task.cancel()
    loop.stop()


async def main():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as executor, multiprocessing.Manager() as manager:
        message_queue = manager.Queue()  # allow message passing between processes
        loop.run_in_executor(executor, run_clock, message_queue)
        loop.run_in_executor(executor, run_server, message_queue)
        loop.run_in_executor(executor, run_temper)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    # shutdown gracefully on Ctrl+C
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: shutdown(loop))

    try:
        loop.run_until_complete(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        loop.close()
