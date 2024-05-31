import asyncio
from concurrent.futures import ProcessPoolExecutor
from threading import Event
import os
import logging
import multiprocessing
import queue
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


exit = Event()

def run_clock(message_queue):
    clock = Clock()
    show_clock = True

    while not exit.is_set():
        # check for messages
        try:
            message = message_queue.get_nowait()
            logging.info('GOT MESSAGE: ' + message)
            show_clock = 'off' not in message
        except queue.Empty:
            pass  # no new messages - continue

        asyncio.run(clock.run(show_clock))
        exit.wait(0.1)


def run_temper():
    """ Sends Homebridge the temperature reading from Temper2 """
    while not exit.is_set():
        try:
            temp = TemperApi.get_data().get('temp')
            req = requests.get(f'http://{HOMEBRIDGE_IP}:{HOMEBRIDGE_PORT}/?accessoryId=temper2sensor&value={temp}')
            logging.info(f'Sent temperature to Homebridge and received code {req.status_code}')
        except Exception as e:
            logging.warning(f'Failed to transmit Temper data to Homebridge: {e}')
        exit.wait(60)


async def main():
    loop = asyncio.get_running_loop()
    executor = ProcessPoolExecutor()
    manager = multiprocessing.Manager()
    
    message_queue = manager.Queue()  # allow message passing between processes
    futures = [
        loop.run_in_executor(executor, run_temper),
        loop.run_in_executor(executor, run_clock, message_queue),
        loop.run_in_executor(executor, run_server, message_queue)
    ]
        
    try:
        await asyncio.gather(*futures)
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        print('Shutting down ProcessPoolExecutor and Queue')
        exit.set()
        executor.shutdown()
        manager.shutdown()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        print("Received exit, exiting")
        loop.close()

