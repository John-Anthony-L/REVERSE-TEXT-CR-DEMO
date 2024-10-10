const uploadForm = document.getElementById('upload-form');
const fileInput = document.getElementById('file-input');
const downloadButton = document.getElementById('download-button');

uploadForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        downloadButton.href = data.download_url;
        downloadButton.textContent = 'Download Reversed';
    } catch (error) {
        console.error('Error uploading file:', error);
    }
});
