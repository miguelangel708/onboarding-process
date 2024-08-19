from flask import Blueprint, request, redirect, url_for, flash, current_app, jsonify
import os
from ..models.validateActions import  validateActions
from datetime import datetime

main = Blueprint("general_api", __name__)


UPLOAD_FOLDER = 'uploads/'  # Path where the files will be saved
MAX_FILE_SIZE = 30 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'} # Permitted extensions
DOCUMENT_VALIDATION = False

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validateFiles(file_front, file_back):    
    #  File size validation in the backend
    if len(file_front.read()) > MAX_FILE_SIZE:
        file_front.seek(0)
        return "The front file is too large. The maximum size allowed is 5 MB.", 400
    file_front.seek(0)
    if len(file_back.read()) > MAX_FILE_SIZE:
        file_back.seek(0)
        return "The front file is too large. The maximum size allowed is 5 MB.", 400
    file_back.seek(0)

    # Validación del tipo de archivo en el backend
    if not allowedFile(file_front.filename):
        return "Front file type not allowed. Only JPEG, JPG and PNG are allowed.", 400
    if not allowedFile(file_back.filename):
        return "Front file type not allowed. Only JPEG, JPG and PNG are allowed.", 400
    
    DOCUMENT_VALIDATION = True


@main.route('/upload', methods=['POST'])
def uploadFile():
    
    # validate that all data have been sent
    try:
        # Obtain form files
        file_front = request.files.get('fileFront')
        file_back = request.files.get('fileBack')
        # Obtain other data from the form
        country = request.form.get('country')
        doc_type = request.form.get('docType')
        accept_terms = request.form.get('acceptTerms') == 'true'  # convert to boolean
    except Exception as e:
        return "not all data are found in the form or error when assigning data", 400

    # validate that the images meet the requirements
    validateFiles(file_front, file_back)

    # Save the images in the 'updates' folder
    if file_front:
        file_front.save(os.path.join(UPLOAD_FOLDER, "front_doc.jpg"))
        print(f'Saved front image')
    
    if file_back:
        file_back.save(os.path.join(UPLOAD_FOLDER, "reverse_doc.jpg"))
        print(f'Backup image saved')
    
    validate_actions = validateActions(DOCUMENT_VALIDATION, country, doc_type, accept_terms)
    validate_actions.pipeline_document_validation()
    

    # Suppose that validation_date is the date in UTC format that you want to convert
    validation_date = validate_actions.validation_date
    # Truncate the microseconds part to 6 digits
    validation_date_truncated = validation_date[:26] + "Z"
    # Truncate the microseconds part to 6 digits
    validation_formatted_date = datetime.strptime(validation_date_truncated, "%Y-%m-%dT%H:%M:%S.%fZ")
    # Format the date and time in the format DD/MM/YYYYYY HH:MM:SS
    validation_formatted_date = validation_formatted_date.strftime("%d/%m/%Y %H:%M:%S")
    
    
    response = {
        'status':validate_actions.validation_status,
        'validation_date':validation_formatted_date,
        'processing_time':validate_actions.processing_time
    }
    
    return jsonify(response), 200
