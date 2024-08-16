from flask import Blueprint, request, redirect, url_for, flash, current_app
import os

main = Blueprint("general_api", __name__)


UPLOAD_FOLDER = 'uploads/'  # Ruta donde se guardarán los archivos
MAX_FILE_SIZE = 30 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'} # Extensiones permitidas

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No se seleccionó ningún archivo.", 400

    file = request.files['file']

    # Validación del tamaño del archivo en el backend
    if len(file.read()) > MAX_FILE_SIZE:
        return "El archivo es demasiado grande. El tamaño máximo permitido es 5 MB.", 400
    
    # Validación del tipo de archivo en el backend
    if not allowed_file(file.filename):
        return "Tipo de archivo no permitido. Solo se permiten JPEG, JPG y PNG.", 400

    file.seek(0)  # Restablece el puntero de lectura del archivo al inicio
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    
    return "Archivo subido con éxito."