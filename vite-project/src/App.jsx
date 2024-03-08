
// App.js
import React, { useState, useEffect } from 'react';
import QRCode from 'qrcode.react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

function App() {
  const [images, setImages] = useState([]);

  useEffect(() => {
    socket.on('newImage', (data) => {
      setImages((prevImages) => [...prevImages, data]);
    });
  }, []);

  return (
    <div>
      <h1>QR Code Generator</h1>
      <QRCode value={`http://localhost:3000/upload`} />
      <h2>Uploaded Images:</h2>
      {images.map((image, index) => (
        <img key={index} src={image} alt={`Uploaded ${index}`} />
      ))}
    </div>
  );
}

export default App;
