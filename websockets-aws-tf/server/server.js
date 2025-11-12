// Minimal WS server based on "ws" + HTTP for health checks
// In Dockerfile:
// - install ws
// - started with: `node server.js`

// creates a simple HTTP and WebSocket server on /ws
const http = require("http");
const { WebSocketServer } = require("ws");

// Port taken from PORT env (see Dockerfile) or defaults to 8080
const PORT = process.env.PORT || 8080;

const server = http.createServer((req, res) => {
  // endpoint used by ALB for health checks:
  if (req.url === "/health") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ ok: true }));
  } else {
    // Welcome page (useful for quick HTTP test)
    res.writeHead(200, { "Content-Type": "text/plain" });
    res.end("WebSocket demo is up. Connect to ws://<ALB-DNS>/ws\n");
  }
});

const wss = new WebSocketServer({ noServer: true });

// Handle WS connections:
wss.on("connection", (ws) => {
  ws.send("hello from ECS - WebSocket server!");

  ws.on("message", (msg) => {
    // Echo + timestamp
    ws.send(`echo: ${msg} @ ${new Date().toISOString()}`);
  });

  ws.on("close", () => {
    // noop but handy for logs
  });
});

// Upgrade HTTP -> WS on the /ws path
server.on("upgrade", (req, socket, head) => {
  if (req.url !== "/ws") {
    socket.destroy();
    return;
  }
  wss.handleUpgrade(req, socket, head, (ws) => {
    wss.emit("connection", ws, req);
  });
});

// Start the server: A single process listens for both HTTP and WebSocket
// traffic on the same port (convenient for ECS + ALB)
server.listen(PORT, () => {
  console.log(`HTTP/WS server listening on :${PORT}`);
});
