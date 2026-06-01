const app = require('./app');
const env = require('./config/env');
const { initDatabase } = require('./config/database');

initDatabase()
  .then(() => {
    app.listen(env.port, () => {
      // eslint-disable-next-line no-console
      console.log(`FootToon backend listening on port ${env.port}`);
    });
  })
  .catch((error) => {
    // eslint-disable-next-line no-console
    console.error('Failed to initialize database', error);
    process.exit(1);
  });
