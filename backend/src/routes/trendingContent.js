const express = require('express');

const router = express.Router();

router.get('/', (req, res) => {
  res.json({
    memes: ['VAR check dance', 'Manager sideline reaction', 'Goalkeeper panic edit'],
    themes: ['Title race meltdown', 'Underdog comeback', 'Transfer deadline chaos'],
    songs: ['Stadium remix challenge', 'Viral chant mashup'],
  });
});

module.exports = router;
