document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío tradicional del formulario

    const fileFront = document.getElementById('fileFront').files[0];
    const fileBack = document.getElementById('fileBack').files[0];
    const maxSize = 30 * 1024 * 1024; // Tamaño máximo permitido en bytes (30 MB)
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png']; // Tipos de archivo permitidos

    if (!fileFront || !fileBack) {
        document.getElementById('status').textContent = 'Debe cargar ambas imágenes (frente y respaldo).';
        document.getElementById('status').style.color = 'red';
        return;
    }

    if (fileFront.size > maxSize || fileBack.size > maxSize) {
        document.getElementById('status').textContent = 'El archivo es demasiado grande. El tamaño máximo permitido es 30 MB.';
        document.getElementById('status').style.color = 'red';
        return;
    }

    if (!allowedTypes.includes(fileFront.type) || !allowedTypes.includes(fileBack.type)) {
        document.getElementById('status').textContent = 'Tipo de archivo no permitido. Solo se permiten JPEG, JPG y PNG.';
        document.getElementById('status').style.color = 'red';
        return;
    }

    

    const acceptTerms = document.getElementById('acceptTerms').checked;

    const formData = new FormData();
    formData.append('fileFront', fileFront);
    formData.append('fileBack', fileBack);
    formData.append('country', document.getElementById('country').value);
    formData.append('docType', document.getElementById('docType').value);
    formData.append('acceptTerms', acceptTerms); // Agrega el valor de la validación

    fetch('http://127.0.0.1:5000/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('status').textContent = 'Documento subido con éxito.';
        document.getElementById('status').style.color = 'green';
        console.log('response:', data);
    })
    .catch(error => {
        document.getElementById('status').textContent = 'Error al subir el documento.';
        document.getElementById('status').style.color = 'red';
        console.error('Error:', error);
    });
});
