const express = require('express');
const cors = require('cors');
const streamApi = require('./api/stream');

const app = express();
app.use(cors());

// Mount the vercel function to the /api/stream route
app.get('/api/stream', streamApi);

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Local dev server running on http://localhost:${PORT}`);
});
