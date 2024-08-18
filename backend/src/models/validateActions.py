from dataclasses import dataclass
import requests
import os 
from dotenv import load_dotenv

class validateActions:
    
    def __init__(self, document_validation, country, document_type, user_authorized):        
        load_dotenv()
        self.TRUORA_APIKEY = os.environ.get("truoraApiKey", "")
        self.url = os.environ.get("truoraDocumentValidationURL", "")
        
        
        self.document_validation = document_validation
        self.country= country
        self.document_type = document_type
        self.user_authorized = user_authorized
        

        
    def pipeline_document_validation(self):
        # 1. conseguir la validación inicial y adquirir así el front_url y back_url
        data = self.createValidation()
        # 2. extraer los enlaces para hacer upload
        front_url = data["instructions"]["front_url"]
        print("front_url: ",front_url)
        reverse_url = data["instructions"]["reverse_url"]
        print("reverse_url: " ,reverse_url)
        # upload del front
        validate_front_upload = self.uploadDocFrontPicture(front_url)
        # upload reverse
        validate_reverse_upload  = self.uploadDocReversePicture(reverse_url)
        # validate the uploads
        # if not (validate_front_upload and validate_reverse_upload): return "error al cargar las images en el pipeline" , 400 
        # extraer el id para la validación 
        validation_id = data["validation_id"]
        # get validation 
        validate_getValidation = self.getValidation(validation_id)
        # validate the getvalidation response
        if not validate_getValidation:
            print("error al acceder a la validación en getValidation")
            return "error al acceder a la validación en getValidation" , 400 
        
        
        
        
        
    def createValidation(self):
        
        headers = {
            "Truora-API-Key": self.TRUORA_APIKEY,
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Parámetros para filtrar datos en una solicitud GET
        params = {
            "type": "document-validation",
            "country": "CO",
            "document_type": "identity-card",
            "user_authorized": "true",
        }

        response = requests.post(self.url, headers=headers, data=params)

        if response.status_code == 200:
            data = response.json()
            print(data)
            return data
        
        else:
            print(f"Error {response}")


    def uploadDocFrontPicture(self, front_url):
                
        image_path = "uploads/front_doc.jpg"
        if not os.path.exists(image_path):
            print(f"Error: El archivo '{image_path}' no existe.")
            return False
        file_size = os.path.getsize(image_path)
        if file_size == 0:
            print(f"Error: El archivo '{image_path}' está vacío.")
            return False
        with open(image_path, 'rb') as image_file:
            print(f"Archivo '{image_path}' leído correctamente. Tamaño: {file_size} bytes.")



        headers = {
            "Truora-API-Key": self.TRUORA_APIKEY,
        }
        
        with open(image_path, 'rb') as image_file:
            print(image_file)
            response = requests.put(front_url, headers=headers, data=image_file)

        if response.status_code == 200:
            data = response.json()
            print("nice upload front document picture" , data)
            return True
        
        else:
            print(f"Error {response.status_code}")
            return False
        

    def uploadDocReversePicture(self, reverse_url):
        
        image_path = "uploads/reverse_doc.jpg"
        
        headers = {
            "Truora-API-Key": self.TRUORA_APIKEY,
        }
        
        with open(image_path, 'rb') as image_file:
            print(image_file)
            response = requests.put(reverse_url, headers=headers, data=image_file)

        if response.status_code == 200:
            data = response.json()
            print("nice upload reverse document picture",data)
            return True
        
        else:
            print(f"Error {response.status_code}")
            return False
  