const express = require('express');
const app = express();
const port = 3000;

app.get('/instagram-webhook', (req, res) => {
  const challenge = req.query['hub.challenge'];
  res.status(200).send(challenge);
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
