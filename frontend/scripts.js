
document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío tradicional del formulario

    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    const maxSize = 30 * 1024 * 1024; // Tamaño máximo permitido en bytes (5 MB)
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png']; // Tipos de archivo permitidos

    if (file.size > maxSize) {
        document.getElementById('status').textContent = 'El archivo es demasiado grande. El tamaño máximo permitido es 5 MB.';
        document.getElementById('status').style.color = 'red';
        return; // Evita el envío si el archivo es demasiado grande
    }

    // Validación del tipo de archivo
    if (!allowedTypes.includes(file.type)) {
        document.getElementById('status').textContent = 'Tipo de archivo no permitido. Solo se permiten JPEG, JPG y PNG.';
        document.getElementById('status').style.color = 'red';
        return; // Evita el envío si el tipo de archivo no es permitido
    }
    
    const formData = new FormData();
    formData.append('file', file);

    fetch('http://127.0.0.1:5000/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('status').textContent = 'Archivo subido con éxito.';
        document.getElementById('status').style.color = 'green';
        console.log('response: ', data);
    })
    .catch(error => {
        document.getElementById('status').textContent = 'Error al subir el archivo.';
        document.getElementById('status').style.color = 'red';
        console.error('Error:', error);
    });
});
