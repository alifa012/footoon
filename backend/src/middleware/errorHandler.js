module.exports = (err, req, res, next) => {
  if (res.headersSent) {
    next(err);
    return;
  }

  const status = err.status || 500;
  res.status(status).json({
    message: err.message || 'Internal server error',
  });
};
