
// App.js
import React, { useState, useEffect } from 'react';
import QRCode from 'qrcode.react';
import io from 'socket.io-client';

const ORIGIN = '';

const socket = io(`${ORIGIN}:5000`);

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
      <QRCode value={`upload`} />
      <a href={`${ORIGIN}/upload`}>/upload</a>
      <h2>Uploaded Images:</h2>
      {images.map((image, index) => (
        <img key={index} src={image} alt={`Uploaded ${index}`} />
      ))}
    </div>
  );
}

export default App;
