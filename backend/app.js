// backend/app.js
const express = require('express');
const axios = require('axios');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();
const app = express();
app.use(cors()); // 解决跨域
app.use(express.json());

// 1. 连接算法层API（Python Flask）
const ALGORITHM_API = 'http://localhost:5000/api';

// 2. 初始化数据库（存储仿真数据，体现数据层）
const db = new sqlite3.Database('../data/simulation.db', (err) => {
    if (err) console.error('数据库连接失败：', err);
    else console.log('数据库连接成功');
    // 创建仿真数据表
    db.run(`CREATE TABLE IF NOT EXISTS simulation_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        distance REAL,
        propagation_loss REAL,
        delay_diff REAL,
        ber REAL,
        voltage REAL,
        temperature REAL,
        depth REAL,
        status TEXT
    )`);
});

// API1：获取融合的设备+信道数据（给前端）
app.get('/api/twin/data', async (req, res) => {
    try {
        // 调用算法层API
        const distance = req.query.distance || 10;
        const [channelRes, deviceRes] = await Promise.all([
            axios.get(`${ALGORITHM_API}/channel/params`, { params: { distance } }),
            axios.get(`${ALGORITHM_API}/device/status`)
        ]);
        // 融合数据
        const data = {
            channel: channelRes.data.data,
            device: deviceRes.data.data,
            distance: distance
        };
        // 存入数据库（体现数据存储，工作量++）
        db.run(`INSERT INTO simulation_data 
            (distance, propagation_loss, delay_diff, ber, voltage, temperature, depth, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
            [distance, data.channel.propagation_loss, data.channel.delay_diff, data.channel.ber,
             data.device.voltage, data.device.temperature, data.device.depth, data.device.status]
        );
        res.json({ code: 200, data });
    } catch (err) {
        res.json({ code: 500, msg: '数据获取失败', err: err.message });
    }
});

// API2：获取历史仿真数据（用于前端绘制曲线）
app.get('/api/twin/history', (req, res) => {
    const limit = req.query.limit || 30; // 取最近30条
    db.all(`SELECT * FROM simulation_data ORDER BY time DESC LIMIT ?`, [limit], (err, rows) => {
        if (err) res.json({ code: 500, msg: '查询失败' });
        else res.json({ code: 200, data: rows.reverse() }); // 反转，按时间正序
    });
});

// 启动后端服务
app.listen(3000, () => {
    console.log('后端服务运行在：http://localhost:3000');
});