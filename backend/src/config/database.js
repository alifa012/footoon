const fs = require('fs');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();
const env = require('./env');

const dbDir = path.dirname(env.dbPath);
if (!fs.existsSync(dbDir)) {
  fs.mkdirSync(dbDir, { recursive: true });
}

const db = new sqlite3.Database(env.dbPath);

const initDatabase = () =>
  new Promise((resolve, reject) => {
    const schemaPath = path.resolve(process.cwd(), 'src', 'db', 'schema.sql');
    fs.readFile(schemaPath, 'utf8', (readErr, schemaSql) => {
      if (readErr) {
        reject(readErr);
        return;
      }

      db.exec(schemaSql, (execErr) => {
        if (execErr) {
          reject(execErr);
          return;
        }
        resolve();
      });
    });
  });

module.exports = {
  db,
  initDatabase,
};
