document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Avoid traditional form submission

    const fileFront = document.getElementById('fileFront').files[0];
    const fileBack = document.getElementById('fileBack').files[0];
    const maxSize = 30 * 1024 * 1024; // Tamaño máximo permitido en bytes (30 MB)
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png']; // Tipos de archivo permitidos

    const statusElement = document.getElementById('status');
    const validationStatusElement = document.getElementById('validation-status');
    const process_time = document.getElementById('process_time')
    const date_time = document.getElementById('date_time')
    


    if (!fileFront || !fileBack) {
        statusElement.textContent = 'You must upload both images (front and back).';
        statusElement.style.color = 'red';
        return;
    }

    if (fileFront.size > maxSize || fileBack.size > maxSize) {
        statusElement.textContent = 'The file is too large. The maximum size allowed is 30 MB.';
        statusElement.style.color = 'red';
        return;
    }

    if (!allowedTypes.includes(fileFront.type) || !allowedTypes.includes(fileBack.type)) {
        statusElement.textContent = 'File type not allowed. Only JPEG, JPG and PNG are allowed.';
        statusElement.style.color = 'red';
        return;
    }

    const acceptTerms = document.getElementById('acceptTerms').checked;

    const formData = new FormData();
    formData.append('fileFront', fileFront);
    formData.append('fileBack', fileBack);
    formData.append('country', document.getElementById('country').value);
    formData.append('docType', document.getElementById('docType').value);
    formData.append('acceptTerms', acceptTerms); // Add validation value

    // Show loading screen
    statusElement.textContent = 'Uploading...';
    statusElement.style.color = 'blue';

    fetch('http://127.0.0.1:5000/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json()) // Switch to response.json() to parse JSON response
    .then(data => {
        // Check the status returned by the API
        if (data.status === 'success') {
            
            statusElement.textContent = 'Document successfully uploaded';
            statusElement.style.color = 'green';
            
            validationStatusElement.textContent = 'Success'
            validationStatusElement.style.backgroundColor = 'green'

            process_time.textContent = data.processing_time + ' Seconds'
            date_time.textContent = data.validation_date 

        } else if (data.status === 'pending') {
            
            statusElement.textContent = 'Error uploading the document.';
            statusElement.style.color = 'red';
            
            validationStatusElement.textContent = 'Denied'
            validationStatusElement.style.backgroundColor = 'red'
            
            date_time.textContent = data.validation_date
            process_time.textContent = 'time exceeded'


        } else if (data.status === 'failure') {
            
            statusElement.textContent = 'Error with the photos. Verify that the uploaded photos are well taken, for this you can consult the following guide to capture documents: https://developer.truora.com/products/digital-identity/document_validation_picture_tips.html.';
            statusElement.style.color = 'red';
            
            validationStatusElement.textContent = 'Denied'
            validationStatusElement.style.backgroundColor = 'red' 
            
            date_time.textContent = data.validation_date
            process_time.textContent = data.processing_time + ' Seconds'


        }
        console.log('response:', data);
    })
    .catch(error => {
        statusElement.textContent = 'Error uploading the document.';
        statusElement.style.color = 'red';
        console.error('Error:', error);
    });
});


document.getElementById('fileFront').addEventListener('change', function(event) {
    var previewFront = document.getElementById('previewFront');
    var file = event.target.files[0];
    
    if (file) {
        var reader = new FileReader();
        
        reader.onload = function(e) {
            previewFront.src = e.target.result;
        };
        
        reader.readAsDataURL(file);
    }
});

document.getElementById('fileBack').addEventListener('change', function(event) {
    var previewBack = document.getElementById('previewBack');
    var file = event.target.files[0];
    
    if (file) {
        var reader = new FileReader();
        
        reader.onload = function(e) {
            previewBack.src = e.target.result;
        };
        
        reader.readAsDataURL(file);
    }
});