
function setCompressionAvailable(value) {
  const compressionCheckbox = document.querySelector("#compression-checkbox");
  compressionCheckbox.clicked = false;
  compressionCheckbox.disabled = value;
}

function checkCompressionEnabled() {
  const compressionCheckbox = document.querySelector("#compression-checkbox");
  return compressionCheckbox.clicked;
}

window.addEventListener("load", function() {
  const overlay = document.getElementById("overlay");
  overlay.style.display = "flex";
  setTimeout(function() {
    overlay.style.display = "none";
  }, 1000);
});

async function compressImage(file, { quality = 1, type = file.type }) {
  // Get as image data
  const imageBitmap = await createImageBitmap(file);

  // Draw to canvas
  const canvas = document.createElement('canvas');
  canvas.width = imageBitmap.width;
  canvas.height = imageBitmap.height;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(imageBitmap, 0, 0);

  // Turn into Blob
  return await new Promise((resolve) =>
    canvas.toBlob(resolve, type, quality)
  );
};

function handleUploadSubmit() {
  const fileInput = document.getElementById('file-input');
  const file = fileInput.files[0];

  if (!file) {
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  fetch('/upload', {
    method: 'POST',
    body: formData
  })
    .catch((error) => {
      console.error('Error:', error);
      alert('File upload failed.');
    });
}

function handleFileSelect(event) {
  const fileInput = event.target;
  const fileName = fileInput.files[0].name;
  const uploadButton = document.getElementById("upload-button");
  const selectImageButton = document.querySelector(".file-label");
  selectImageButton.style = "border-style: solid;"
  selectImageButton.textContent = fileName;

  const isPdf = fileName.endsWith('pdf');
  setCompressionAvailable(isPdf);

  uploadButton.classList.add("selected");

}

function showAlert(message) {
  const alertContainer = document.getElementById('alert-container');
  const alertBox = document.createElement('div');
  alertBox.classList.add('alert-box');
  alertBox.innerHTML = `
          <span>${message}</span>
          <span class="close-icon">&times;</span>
        `;

  alertContainer.appendChild(alertBox);

  setTimeout(() => {
    alertBox.classList.add('show');
  }, 100);

  const closeIcon = alertBox.querySelector('.close-icon');
  closeIcon.addEventListener('click', () => {
    alertBox.classList.remove('show');
    setTimeout(() => {
      alertBox.remove();
    }, 300);
  });
}
