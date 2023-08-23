// Create the endpoint for your webhook

app.post("/instaglam-webhook", (req, res) => {
  let body = req.body;

  console.log(`\u{1F7EA} Received webhook:`);
  console.dir(body, { depth: null });
    
...
