const express = require('express');
const { db } = require('../config/database');

const router = express.Router();

router.get('/', (req, res, next) => {
  db.all(
    'SELECT id, title, premise, generated_script AS generatedScript, tags, created_at AS createdAt FROM script_ideas ORDER BY created_at DESC',
    [],
    (err, rows) => {
      if (err) {
        next(err);
        return;
      }
      res.json(rows);
    },
  );
});

router.post('/', (req, res, next) => {
  const { title, premise, generatedScript, tags = '' } = req.body || {};

  if (!title || !premise || !generatedScript) {
    res.status(400).json({ message: 'title, premise, and generatedScript are required' });
    return;
  }

  db.run(
    'INSERT INTO script_ideas (title, premise, generated_script, tags) VALUES (?, ?, ?, ?)',
    [title, premise, generatedScript, tags],
    function onInsert(err) {
      if (err) {
        next(err);
        return;
      }

      res.status(201).json({
        id: this.lastID,
        title,
        premise,
        generatedScript,
        tags,
      });
    },
  );
});

module.exports = router;
