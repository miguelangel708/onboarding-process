from flask import Blueprint, request, redirect, url_for, flash, current_app, jsonify
import os
from ..models.validateActions import  validateActions

main = Blueprint("general_api", __name__)


UPLOAD_FOLDER = 'uploads/'  # Ruta donde se guardarán los archivos
MAX_FILE_SIZE = 30 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'} # Extensiones permitidas
DOCUMENT_VALIDATION = False

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validateFiles(file_front, file_back):    
    #  Validación del tamaño del archivo en el backend
    if len(file_front.read()) > MAX_FILE_SIZE:
        return "El archivo frontal es demasiado grande. El tamaño máximo permitido es 5 MB.", 400
    if len(file_back.read()) > MAX_FILE_SIZE:
        return "El archivo frontal es demasiado grande. El tamaño máximo permitido es 5 MB.", 400
    
    # Validación del tipo de archivo en el backend
    if not allowed_file(file_front.filename):
        return "Tipo de archivo frontal no permitido. Solo se permiten JPEG, JPG y PNG.", 400
    if not allowed_file(file_back.filename):
        return "Tipo de archivo trasero no permitido. Solo se permiten JPEG, JPG y PNG.", 400
    
    DOCUMENT_VALIDATION = True


@main.route('/upload', methods=['POST'])
def upload_file():
    
    neededData = ['fileFront','fileBack','country','docType','acceptTerms']
    
    # validar que se hayan enviado todos los datos
    try:
        # Obtener los archivos del formulario
        file_front = request.files.get('fileFront')
        file_back = request.files.get('fileBack')
        # Obtener otros datos del formulario
        country = request.form.get('country')
        doc_type = request.form.get('docType')
        accept_terms = request.form.get('acceptTerms') == 'true'  # Convertir a booleano
    except Exception as e:
        return "no se encuentran todos los datos en el formulario o error al asignarlos", 400

    # validar que las imagenes cumplan los requisitos
    validateFiles(file_front, file_back)

    # Imprimir todos los datos recibidos
    print(f'País: {country}')
    print(f'Tipo de documento: {doc_type}')
    print(f'Términos aceptados: {accept_terms}')
    
    # Guardar las imágenes en la carpeta 'updates'
    if file_front:
        file_front.save(os.path.join(UPLOAD_FOLDER, file_front.filename))
        print(f'Imagen de frente guardada en: {os.path.join(UPLOAD_FOLDER, file_front.filename)}')
    
    if file_back:
        file_back.save(os.path.join(UPLOAD_FOLDER, file_back.filename))
        print(f'Imagen de respaldo guardada en: {os.path.join(UPLOAD_FOLDER, file_back.filename)}')
    
    validate_actions = validateActions(DOCUMENT_VALIDATION, country, doc_type, accept_terms)
    validate_actions.pipeline_document_validation()
    
    return jsonify({'message': 'Datos recibidos y archivos guardados con éxito'}), 200
