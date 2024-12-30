from algoritm.algoritms_one import start, Range_99_7, Range_95, Range_68, Mean, Sigma, Convert, detect_trend_change

BLUE = '\033[94m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def Color(price):
    if price[-1] / price[-2] * 100 - 100 > 0:
        return ['\033[92m', '↑']
    else:
        return ['\033[91m', '↓']

def Color2(price):
    trend, deviation = detect_trend_change(price)
        
    # Определяем цвет и символ
    if "нисходящий" in trend:
        return [trend, '↓', '\033[91m', deviation]
    elif "восходящий" in trend:
        return [trend, '↑', '\033[92m', deviation]
    else:
        return [trend, '-', '\033[90m', deviation]

def logs(price, timestamp):
    print(f"▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
    print(f"\t┌────────────────────────────────────────────────────────────────────────┐")
    print(f"\t│Среднее значение: \t\t\t {round(Mean(price), 3)} \t\t\t │")
    print(f"\t│Стандартное отклонение (σ): \t\t {round(Sigma(price), 5)} \t\t\t │")
    print(f"\t└────────────────────────────────────────────────────────────────────────┘")
    print(f"\t┌────────────────────────────────────────────────────────────────────────┐")
    print(f"\t│{RED}Диапазон для 68% вероятности:{RESET} \t\t {Convert(Range_68(price))} \t │")
    print(f"\t│{YELLOW}Диапазон для 95% вероятности:{RESET} \t\t {Convert(Range_95(price))} \t │")
    print(f"\t│{GREEN}Диапазон для 99.7% вероятности:{RESET} \t {Convert(Range_99_7(price))} \t │")
    print(f"\t└────────────────────────────────────────────────────────────────────────┘")
    print(f"\t┌────────────────────────────────────────────────────────────────────────┐")
    print(f"\t│Прошлая цена: \t\t\t\t {round(price[-2], 5)} \t\t\t │")
    print(f"\t│Текущая цена: \t\t\t\t {round(price[-1], 5)} \t\t\t │")
    print(f"\t│Отношение прошлой к текущей цене:\t {Color(price)[0]}{round(price[-1]/price[-2]*100-100, 5)}% \t {Color(price)[1]}{RESET} \t\t │")
    print(f"\t└────────────────────────────────────────────────────────────────────────┘")
    print(f"\t┌────────────────────────────────────────────────────────────────────────┐")
    print(f"\t│{Color2(price)[2]}Тип тренда: \t\t\t\t {Color2(price)[0]} \t {Color2(price)[1]}{RESET} \t\t │")
    print(f"\t└────────────────────────────────────────────────────────────────────────┘")
    
    # print(f"\t┌────────────────────────────────────────────────────────────────────────┐")
    # print(f"\t│{YELLOW}Предположительная цена: \t\t {round(start(price, timestamp), 5)}{RESET} \t\t\t │")
    # print(f"\t└────────────────────────────────────────────────────────────────────────┘")
    