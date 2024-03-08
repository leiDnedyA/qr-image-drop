
// App.js
import React, { useState, useEffect } from 'react';
import QRCode from 'qrcode.react';
import io from 'socket.io-client';

const ORIGIN = window.location.origin;

const SOCKET_PORT = 5000;
const SOCKET_URL = `${window.location.protocol}//${window.location.hostname}:${SOCKET_PORT}`;
const socket = io(SOCKET_URL);

console.log(SOCKET_URL);


function App() {
  const [images, setImages] = useState([]);

  console.log('test')
  useEffect(() => {
    socket.on('newImage', (data) => {
      setImages((prevImages) => [...prevImages, data]);
    });
  }, []);

  return (
    <div>
      <h1>QR Code Generator</h1>
      <QRCode value={`${ORIGIN}/upload`} />
      <a href={`${ORIGIN}/upload`}>/upload</a>
      <h2>Uploaded Images:</h2>
      {images.map((image, index) => (
        <img key={index} src={image} alt={`Uploaded ${index}`} />
      ))}
    </div>
  );
}

export default App;
