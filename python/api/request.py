import requests
from dotenv import load_dotenv
import os

load_dotenv()


BASE_URL = "http://localhost:3000/api"

def get_all_btc_data():
    """
    Получает массив всех записей BTC с сервера.
    """
    try:
        response = requests.get(f"{BASE_URL}/btc")
        response.raise_for_status()
        data = response.json()
        return data[-int(os.getenv("MANY")):]
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе всех данных BTC: {e}")
        return None


def get_latest_btc_data():
    """
    Получает последнюю запись BTC с сервера.
    """
    try:
        response = requests.get(f"{BASE_URL}/btc/latest")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе последней записи BTC: {e}")
        return None
    
