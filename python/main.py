import time
from api import get_all_btc_data
from algoritm.algoritms_one import ToTime, ToPrice
from logs import logs as Logs
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    while True:
        try:
            convertToPrice = ToPrice(get_all_btc_data())
            convertToTime = ToTime(get_all_btc_data())

            Logs(convertToPrice, convertToTime)
            time.sleep(int(os.getenv('DATA_REFRESH')))
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()