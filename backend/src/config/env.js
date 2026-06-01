const path = require('path');
const dotenv = require('dotenv');

dotenv.config({ path: path.resolve(process.cwd(), '.env') });

module.exports = {
  nodeEnv: process.env.NODE_ENV || 'development',
  port: Number(process.env.PORT) || 4000,
  footballApiUrl: process.env.FOOTBALL_API_URL || 'https://api.example.com/football',
  footballApiKey: process.env.FOOTBALL_API_KEY || '',
  trendSourceUrl: process.env.TREND_SOURCE_URL || 'https://example.com/trends',
  dbPath: process.env.DB_PATH || path.resolve(process.cwd(), 'data', 'footoon.sqlite'),
};
