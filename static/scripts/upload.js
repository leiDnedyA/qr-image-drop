function clearInputs() {
  const compressionCheckbox = document.querySelector("#compression-checkbox");
  compressionCheckbox.checked = false;
  const uploadButton = document.getElementById("upload-button");
  uploadButton.classList.remove("selected");
  const fileInput = document.getElementById("file-input");
  fileInput.value = null;
  const selectImageButton = document.querySelector(".file-label");
  selectImageButton.style = "border-style: solid;"
  selectImageButton.textContent = "✉️ Choose a file";
}

async function playAnimation() {
  const overlay = document.getElementById("overlay");
  overlay.style.display = "flex";
  return new Promise((res) => {
    setTimeout(function() {
      overlay.style.display = "none";
      res();
    }, 1000);
  });
}

function getCurrentSessionId() {
  let params = new URL(document.location.toString()).searchParams;
  return params.get("session_id");
}

function setCompressionAvailable(value) {
  const compressionCheckbox = document.querySelector("#compression-checkbox");
  compressionCheckbox.clicked = false;
  compressionCheckbox.disabled = value;
}

function checkCompressionEnabled() {
  const compressionCheckbox = document.querySelector("#compression-checkbox");
  return compressionCheckbox.checked;
}

window.addEventListener("load", playAnimation);

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
  const blob = await new Promise((resolve) =>
    canvas.toBlob(resolve, type, quality)
  );

  // Turn Blob into File
  return new File([blob], file.name, {
    type: blob.type,
  });
};

async function handleUploadSubmit(event) {
  event.preventDefault();
  const fileInput = document.getElementById('file-input');
  let file = fileInput.files[0];

  if (!file) {
    return;
  }

  if (checkCompressionEnabled()) {
    file = await compressImage(file, { quality: .2, type: 'image/jpeg' });
  }

  const formData = new FormData();
  formData.append('file', file);

  await fetch(`/upload?session_id=${getCurrentSessionId()}`, {
    method: 'POST',
    body: formData
  })
    .catch((error) => {
      console.error('Error:', error);
      alert('File upload failed.');
    });

  playAnimation();
  clearInputs();
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
