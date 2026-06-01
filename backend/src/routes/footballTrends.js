const express = require('express');

const router = express.Router();

router.get('/', (req, res) => {
  res.json({
    players: ['Kylian Mbappé', 'Erling Haaland', 'Jude Bellingham'],
    matches: ['Champions League Final', 'El Clásico', 'Manchester Derby'],
    transfers: ['Star striker linked to Serie A', 'Young winger signs new deal'],
  });
});

module.exports = router;
