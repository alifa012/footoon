const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const footballTrendsRoute = require('./routes/footballTrends');
const trendingContentRoute = require('./routes/trendingContent');
const scriptGeneratorRoute = require('./routes/scriptGenerator');
const scriptsRoute = require('./routes/scripts');
const notFound = require('./middleware/notFound');
const errorHandler = require('./middleware/errorHandler');

const app = express();

app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.use('/api/football-trends', footballTrendsRoute);
app.use('/api/trending-content', trendingContentRoute);
app.use('/api/script-generator', scriptGeneratorRoute);
app.use('/api/scripts', scriptsRoute);

app.use(notFound);
app.use(errorHandler);

module.exports = app;
