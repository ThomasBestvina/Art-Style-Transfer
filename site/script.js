// Handle file input change event
document.getElementById('imageInput').addEventListener('change', (event) => {
    const imageInput = event.target;
    const originalImage = document.getElementById('originalImage');

    if (imageInput.files && imageInput.files[0]) {
        const reader = new FileReader();

        reader.onload = (e) => {
            originalImage.src = e.target.result;
            originalImage.style.display = 'block';
        };

        reader.readAsDataURL(imageInput.files[0]);
    }
});

// Handle the process button click event
document.getElementById('processBtn').addEventListener('click', async () => {
    const imageInput = document.getElementById('imageInput');
    const genNumber = document.getElementById('genNumber').value;
    const outputImage = document.getElementById('outputImage');

    if (!imageInput.files.length) {
        alert('Please select an image.');
        return;
    }

    const file = imageInput.files[0];
    const formData = new FormData();
    formData.append('image', file);

    // Update the API URL to use the live backend
    const apiUrl = `http://localhost:5000`;

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Failed to process image.');
        }

        const responseText = await response.text();
        const imageUrl = responseText.slice(10, -2);

        outputImage.src = imageUrl;
        outputImage.style.display = 'block';
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
});
