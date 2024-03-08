// server.js
const express = require('express');
const http = require('http');
const socketIO = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIO(server, {
  cors: {
    origin: "*"
  }
});

io.on('connection', (socket) => {
  console.log('New client connected');

  socket.on('uploadImage', (data) => {
    io.emit('newImage', data);
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

const port = 5000;
server.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
