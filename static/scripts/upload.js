
window.addEventListener("load", function() {
  const overlay = document.getElementById("overlay");
  overlay.style.display = "flex";
  setTimeout(function() {
    overlay.style.display = "none";
  }, 1000);
});

function handleUploadSubmit() {
  const fileInput = document.getElementById('file-input');
  const file = fileInput.files[0];

  // Check if a file was selected
  if (!file) {
    alert('Please select a file!');
    return;
  }

  const formData = new FormData();
  formData.append('file', file); // Append the file to the form data

  // Make the POST request using fetch
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
