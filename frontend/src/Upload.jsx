import React, { useState } from 'react';
import io from 'socket.io-client';

const socket = io();

function Upload() {
  const [selectedImage, setSelectedImage] = useState(null);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
      setSelectedImage(reader.result);
      socket.emit('uploadImage', reader.result);
    };
  };

  return (
    <div>
      <h1>Upload Image</h1>
      <input type="file" accept="image/*" onChange={handleImageUpload} />
      {selectedImage && <img src={selectedImage} alt="Uploaded" />}
    </div>
  );
}

export default Upload;