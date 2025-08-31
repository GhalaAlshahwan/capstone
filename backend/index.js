const express = require('express');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

app.use(cors());
app.use(bodyParser.json());

// Open or create SQLite DB
const db = new sqlite3.Database('fruit.db', (err) => {
  if (err) console.error(err.message);
  else console.log('Connected to SQLite DB.');
});

// Create table if not exists
db.run(`CREATE TABLE IF NOT EXISTS detections (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fruit TEXT,
  area REAL,
  timestamp TEXT
)`);

// POST endpoint to receive detection
app.post('/log-detection', (req, res) => {
  const { fruit, area, timestamp } = req.body;
  db.run(`INSERT INTO detections (fruit, area, timestamp) VALUES (?, ?, ?)`,
    [fruit, area, timestamp],
    function(err) {
      if (err) return res.status(500).send(err.message);
      res.send({ message: 'Logged!', id: this.lastID });
    });
});

app.listen(port, () => console.log(`Server running on http://localhost:${port}`));
