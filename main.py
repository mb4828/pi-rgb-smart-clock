import time
from api import get_all


def main():
    while True:
        api_data = get_all()
        print(f'{api_data.get("local_time")} | {api_data.get("local_date")}')
        if 'weather' in api_data:
            print(f'{api_data.get("weather").get("temp")}° | {api_data.get("weather").get("humidity")}%')
        if 'forecast' in api_data:
            print(api_data.get("forecast"))
        if 'stocks' in api_data:
            print(' | '.join([f'{stock["name"]}: {stock["price"]} {stock["points"]} [{stock["percent"]}]' for stock in api_data.get("stocks")]))
        print()
        time.sleep(1)

if __name__ == '__main__':
    main()
