import multiprocessing
import queue
import time
from api import get_all
from server import run_server


def run_clock(message_queue):
    while True:
        # check for messages
        try:
            message = message_queue.get_nowait()
            print('GOT MESSAGE: ' + message)
        except queue.Empty:
            pass  # no new messages - continue

        # get data from apis
        api_data = get_all()

        # update clock display
        print(f'{api_data.get("local_time")} | {api_data.get("local_date")}')
        if 'weather' in api_data:
            print(f'{api_data.get("weather").get("temp")}° | {api_data.get("weather").get("humidity")}%')
        if 'forecast' in api_data:
            print(api_data.get("forecast"))
        if 'stocks' in api_data:
            print(
                ' | '.join(
                    [f'{stock["name"]}: {stock["price"]} {stock["points"]} [{stock["percent"]}]'
                     for stock in api_data.get("stocks")]))
        if 'temper' in api_data:
            print(api_data.get("temper"))
        print()

        time.sleep(1)


def main():
    message_queue = multiprocessing.Queue()

    clock_proc = multiprocessing.Process(target=run_clock, args=(message_queue,))
    clock_proc.start()

    try:
        run_server(message_queue)
    except KeyboardInterrupt:
        pass  # Ctrl+C to terminate Flask
    finally:
        clock_proc.terminate()
        clock_proc.join()


if __name__ == '__main__':
    main()
