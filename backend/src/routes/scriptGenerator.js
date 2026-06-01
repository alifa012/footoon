const express = require('express');
const { buildScriptIdea } = require('../services/scriptGenerator');

const router = express.Router();

router.post('/', (req, res) => {
  const { theme, players, meme, song } = req.body || {};
  const scriptIdea = buildScriptIdea({ theme, players, meme, song });
  res.status(201).json(scriptIdea);
});

module.exports = router;
