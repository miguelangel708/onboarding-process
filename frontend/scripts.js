document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío tradicional del formulario

    const fileFront = document.getElementById('fileFront').files[0];
    const fileBack = document.getElementById('fileBack').files[0];
    const maxSize = 30 * 1024 * 1024; // Tamaño máximo permitido en bytes (30 MB)
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png']; // Tipos de archivo permitidos

    const statusElement = document.getElementById('status');

    if (!fileFront || !fileBack) {
        statusElement.textContent = 'Debe cargar ambas imágenes (frente y respaldo).';
        statusElement.style.color = 'red';
        return;
    }

    if (fileFront.size > maxSize || fileBack.size > maxSize) {
        statusElement.textContent = 'El archivo es demasiado grande. El tamaño máximo permitido es 30 MB.';
        statusElement.style.color = 'red';
        return;
    }

    if (!allowedTypes.includes(fileFront.type) || !allowedTypes.includes(fileBack.type)) {
        statusElement.textContent = 'Tipo de archivo no permitido. Solo se permiten JPEG, JPG y PNG.';
        statusElement.style.color = 'red';
        return;
    }

    const acceptTerms = document.getElementById('acceptTerms').checked;

    const formData = new FormData();
    formData.append('fileFront', fileFront);
    formData.append('fileBack', fileBack);
    formData.append('country', document.getElementById('country').value);
    formData.append('docType', document.getElementById('docType').value);
    formData.append('acceptTerms', acceptTerms); // Agrega el valor de la validación

    // Mostrar pantalla de carga
    statusElement.textContent = 'Uploading...';
    statusElement.style.color = 'blue';

    fetch('http://127.0.0.1:5000/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json()) // Cambiar a response.json() para analizar la respuesta JSON
    .then(data => {
        // Comprobar el estado devuelto por la API
        if (data.status === 'success') {
            statusElement.textContent = 'Documento subido con éxito.';
            statusElement.style.color = 'green';
        } else if (data.status === 'pending') {
            statusElement.textContent = 'Error al subir el documento.';
            statusElement.style.color = 'red';
        } else if (data.status === 'failure') {
            statusElement.textContent = 'Error con las fotos. Verifique que las fotos subidas, se encuentren bien tomadas, para ello puede consultar la siguiente guia para capturar documentos: https://developer.truora.com/products/digital-identity/document_validation_picture_tips.html.';
            statusElement.style.color = 'red';
        }
        console.log('response:', data);
    })
    .catch(error => {
        statusElement.textContent = 'Error al subir el documento.';
        statusElement.style.color = 'red';
        console.error('Error:', error);
    });
});
