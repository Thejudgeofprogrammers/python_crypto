const axios = require('axios');
const pool = require('./db');

async function fetchBTCData() {
  try {
    const response = await axios.get('https://api.binance.com/api/v3/avgPrice', {
      params: { symbol: 'BTCUSDT' },
    });

    const price = parseFloat(response.data.price);
    const timestamp = new Date();

    const result = await pool.query(
      'INSERT INTO btc_data (price, timestamp) VALUES ($1, $2) RETURNING id',
      [price, timestamp]
    );

    console.log(`Сохранено: ID ${result.rows[0].id}, Цена ${price}, Время ${timestamp}`);
  } catch (error) {
    console.error('Ошибка при получении данных BTC:', error.message);
  }
}

module.exports = fetchBTCData;