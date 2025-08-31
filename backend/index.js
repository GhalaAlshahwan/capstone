const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');

const app = express();
app.use(cors()); 
app.use(express.json()); 

const db = new sqlite3.Database('fruit_logs.db');

db.run(`CREATE TABLE IF NOT EXISTS logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fruit TEXT,
  area REAL,
  timestamp TEXT
)`);

app.post('/logs', (req, res) => {
  const { fruit, area, timestamp } = req.body;
  db.run(
    `INSERT INTO logs (fruit, area, timestamp) VALUES (?, ?, ?)`,
    [fruit, area, timestamp],
    function(err) {
      if (err) return res.status(500).send(err.message);
      res.send({ success: true, id: this.lastID });
    }
  );
});

app.get('/logs', (req, res) => {
  db.all(`SELECT * FROM logs ORDER BY id DESC LIMIT 100`, [], (err, rows) => {
    if (err) return res.status(500).send(err.message);
    res.send(rows);
  });
});

app.listen(3000, () => console.log('Backend running on port 3000'));
