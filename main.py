import time
from api import get_data


def main():
    while True:
        api_data = get_data()
        print(f'{api_data.get('local_time')} | {api_data.get('local_date')}')
        print(f'{api_data.get('weather').get('temp')}° | {api_data.get('weather').get('humidity')}%')
        print(' | '.join([f'{stock['ticker']}: {stock['price']} ({stock['change']})' for stock in api_data.get('stocks')]))
        time.sleep(1)

if __name__ == '__main__':
    main()