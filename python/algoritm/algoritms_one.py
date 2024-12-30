import numpy as np
from decimal import Decimal, getcontext, ROUND_HALF_UP
from datetime import datetime
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
getcontext().prec = 50

def detect_trend_change(prices, short_window=int(os.getenv("SHORT_WINDOW")), long_window=int(os.getenv("LONG_WINDOW"))):
    """
    Определяет изменение тренда на основе процентного отклонения и пересечения SMA.
    
    :param prices: Список цен (list или pandas.Series)
    :param short_window: Окно для быстрой скользящей средней
    :param long_window: Окно для медленной скользящей средней
    :return: Тренд ("восходящий", "нисходящий", "смена тренда")
    """
    if len(prices) < max(short_window, long_window):
        raise ValueError("Количество данных меньше максимального окна для скользящих средних.")
    
    # Преобразуем все цены в Decimal
    prices = [Decimal(price) if not isinstance(price, Decimal) else price for price in prices]
  
    # Создаем DataFrame и рассчитываем SMA
    df = pd.DataFrame(prices, columns=['Price'])
    df['Short_SMA'] = df['Price'].rolling(window=short_window).mean()
    df['Long_SMA'] = df['Price'].rolling(window=long_window).mean()
    
    # Преобразуем все вычисленные SMA в Decimal
    df['Short_SMA'] = df['Short_SMA'].apply(lambda x: Decimal(x) if not isinstance(x, Decimal) else x)
    df['Long_SMA'] = df['Long_SMA'].apply(lambda x: Decimal(x) if not isinstance(x, Decimal) else x)
    
    # Рассчитываем отклонение текущей цены от долгосрочной SMA
    df['Deviation'] = ((df['Price'] - df['Long_SMA']) / df['Long_SMA']) * Decimal(100)  # Преобразование 100 в Decimal

    # Определяем текущий тренд
    last_short_sma = df['Short_SMA'].iloc[-1]
    last_long_sma = df['Long_SMA'].iloc[-1]
    
    if last_short_sma > last_long_sma:
        trend = "восходящий"
    elif last_short_sma < last_long_sma:
        trend = "нисходящий"
    else:
        trend = "нейтральный"
    
    # Проверка на смену тренда (пересечение SMA)
    if df['Short_SMA'].iloc[-2] > df['Long_SMA'].iloc[-2] and last_short_sma < last_long_sma:
        trend = "смена тренда: нисходящий"
    elif df['Short_SMA'].iloc[-2] < df['Long_SMA'].iloc[-2] and last_short_sma > last_long_sma:
        trend = "смена тренда: восходящий"
    
    return [trend, df['Deviation'].iloc[-1]]
    

def convert_timestamp_to_number(timestamp):
    """
    Преобразует строку timestamp в число (Unix timestamp).
    """
    timestamp_format = "%Y-%m-%dT%H:%M:%S.%fZ"  # Учитываем миллисекунды и символ 'Z'
    try:
        # Преобразуем строку в datetime объект
        dt = datetime.strptime(timestamp, timestamp_format)
        # Преобразуем в Unix timestamp (секунды с 1970-01-01)
        return int(dt.timestamp())
    except ValueError as e:
        print(f"Ошибка при преобразовании timestamp: {timestamp} -> {e}")
        return None

def algoritms_one(data):
    """
    Основной алгоритм, который обрабатывает входные данные.
    Преобразует значения в тип Decimal для высокой точности.
    """
    result = []
    if not data:
        print("После удаления дубликатов данные пусты!")
        return []
    
    for item in data:
        try:
            # Проверка, что элемент является словарем и содержит 'price' и 'timestamp'
            if isinstance(item, dict) and 'price' in item and 'timestamp' in item:
                price = Decimal(item['price'])  # Преобразуем 'price' в Decimal для высокой точности
                timestamp = convert_timestamp_to_number(item['timestamp'])  # Преобразуем 'timestamp' в число (Unix timestamp)
            else:
                print(f"Неверный формат элемента: {item}")
                continue
            
            if timestamp is None:
                print(f"Ошибка при преобразовании timestamp для элемента: {item}")
                continue
            
            result.append([price, timestamp])
        except Exception as e:
            print(f"Ошибка при обработке элемента {item}: {e}")
    
    return result

def calculate_differences(data):
    """
    Вычисляет конечные разности для массива данных.
    :param data: Список данных с ценой и временной меткой
    :return: Массив конечных разностей
    """
    n = len(data)
    differences = np.zeros((n, n), dtype=object)  # Массив для хранения конечных разностей

    for i in range(n):
        differences[i][0] = data[i][0]  # Начальная цена в первом столбце

    for j in range(1, n):  # Для каждого уровня разностей
        for i in range(n - j):  # Проходим по всем элементам
            try:
                # Разности между текущими и предыдущими значениями
                denominator = Decimal(data[i + j][1]) - Decimal(data[i][1])
                if denominator == 0:
                    differences[i][j] = Decimal(0)  # Если делитель 0, то разность равна 0
                else:
                    differences[i][j] = (differences[i + 1][j - 1] - differences[i][j - 1]) / denominator
            except Exception as e:
                print(f"Ошибка при вычислении разности для i={i}, j={j}: {e}")
                differences[i][j] = Decimal(0)

    return differences

def newton_polynomial(price, timestamp, x):
    """
    Строит значение полинома Ньютона в точке x, используя Decimal для точности.
    :param price: Список цен (тип Decimal)
    :param timestamp: Список временных меток (тип int)
    :param x: Точка, в которой вычисляется значение полинома
    :return: Значение полинома Ньютона в точке x
    """
    if len(price) != len(timestamp):
        raise ValueError("Длины массивов price и timestamp должны совпадать")
    
    # Объединяем данные в формат [[price, timestamp], ...]
    data = [[price[i], timestamp[i]] for i in range(len(price))]
    
    differences = calculate_differences(data)  # Получаем конечные разности
    n = len(data)
    result = differences[0][0]  # Начальная сумма - это первый элемент

    product = Decimal(1)
    
    for i in range(1, n):
        product *= (Decimal(x) - Decimal(timestamp[i - 1]))  # Умножаем на разницу с предыдущей временной меткой
        result += differences[0][i] * product  # Добавляем вклад текущей разности
    
    return result


def Mean(data):
    return np.mean(data)


def Sigma(data):
    return np.std(data)


def Range_68(data):
    mean = np.mean(data)
    sigma = Sigma(data)

    range_68 = (round(mean - sigma, 5), round(mean + sigma, 5))  # 68% диапазон

    return range_68

    
def Range_95(data):
    mean = np.mean(data)
    sigma = Sigma(data)

    range_95 = (round(mean - 2 * sigma, 5), round(mean + 2 * sigma, 5))  # 95% диапазон

    return range_95

    
def Range_99_7(data):
    mean = np.mean(data)
    sigma = Sigma(data)

    range_99_7 = (round(mean - 3 * sigma, 5), round(mean + 3 * sigma, 5))  # 99.7% диапазон

    return range_99_7


def ToPrice(data_array):
    data = algoritms_one(data_array)
    prices = [item[0] for item in data]
    return prices


def ToTime(data_array):
    data = algoritms_one(data_array)
    timestamp = [item[1] for item in data]
    return timestamp


def start(price, timestamp):
    """
    Основной процесс для вычислений с использованием Decimal для точности.
    """
    try:
        future_time = timestamp[-1] + int(os.getenv("FUTURE"))
        polynom = newton_polynomial(price, timestamp, future_time)
        return polynom
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


def Convert(Range):
    return f"({Range[0]:.5f}, {Range[1]:.5f})"
