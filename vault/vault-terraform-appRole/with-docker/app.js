console.log("DB_USERNAME:", process.env.DB_USERNAME);
console.log("DB_PASSWORD:", process.env.DB_PASSWORD);

require('http').createServer((req, res) => {
  res.end("Check console for env vars!");
}).listen(3000);
