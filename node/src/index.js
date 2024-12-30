console.clear()
const dotenv = require('dotenv');
dotenv.config();
const pool = require('./db');
const fetchBTCData = require('./btc-fetcher');
const express = require('express')


const app = express()
const port = process.env.PORT

setInterval(fetchBTCData, 10000);

app.get('/api/btc', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM btc_data ORDER BY id ASC');
        res.json(result.rows);
    } catch (error) {
        res.status(500).json({ error: 'Ошибка при получении данных' });
    }
});

app.get('/api/btc/latest', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM btc_data ORDER BY id DESC LIMIT 1');
        res.json(result.rows[0]);
    } catch (error) {
        res.status(500).json({ error: 'Ошибка при получении данных' });
    }
});

app.listen(port, () => {
    console.log(`Сервер запущен на http://localhost:${port}`);
});