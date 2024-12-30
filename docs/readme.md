Таблица БД

## Уровень 0

**Таблица 0**
```ts
{
    capital_btc: float,         // Капитал в BTC
    capital_usd: float          // Капитал в Долларах
}
```

## Уровень 1

**Таблица 1**
```ts
{
    candle_id: int,             // Id свечки (Primary Key)
    price: float,               // Стоимость в BTC
    timestamp: Date,            // Дата
}[]
```

## Уровень 2

**Таблица 2**
```ts
{
    candle_id: int,             // Id свечки (Foreign Key)
    math_expectation: float,    // Математическое ожидание
    volatility: float,               // Дисперсия
    norm_distribution: float
}[]
```

