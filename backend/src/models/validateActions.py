from dataclasses import dataclass
import requests
import os 
from dotenv import load_dotenv
import time


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
        reverse_url = data["instructions"]["reverse_url"]
        # upload del front
        validate_front_upload = self.uploadDocFrontPicture(front_url)
        # upload reverse
        validate_reverse_upload  = self.uploadDocReversePicture(reverse_url)
        # validate the uploads
        if not (validate_front_upload and validate_reverse_upload): return "error al cargar las images en el pipeline" , 400 
        # extraer el id para la validación 
        validation_id = data["validation_id"]
        # get validation
        final_validation_status = self.check_validation_status(validation_id)
        return final_validation_status
        
        
    def createValidation(self):
        
        headers = {
            "Truora-API-Key": self.TRUORA_APIKEY,
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Parámetros para filtrar datos en una solicitud GET
        params = {
            "type": "document-validation",
            "country": self.country,
            "document_type": self.document_type,
            "user_authorized": self.user_authorized,
        }

        response = requests.post(self.url, headers=headers, data=params)

        if response.status_code == 200:
            data = response.json()
            print("validation created with id: ", data["validation_id"])
            return data
        
        else:
            print(f"Error {response}")


    def uploadDocFrontPicture(self, front_url):
                
        image_path = "uploads/front_doc.jpg"
       
        headers = {
            "Truora-API-Key": self.TRUORA_APIKEY,
        }
        
        with open(image_path, 'rb') as image_file:
            response = requests.put(front_url, headers=headers, data=image_file)

        if response.status_code == 200:
            data = response.json()
            print("nice upload front document picture")
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
            response = requests.put(reverse_url, headers=headers, data=image_file)

        if response.status_code == 200:
            data = response.json()
            print("nice upload reverse document picture")
            return True
        
        else:
            print(f"Error {response.status_code}")
            return False
  
        
    def getValidation(self, validation_id):
        
        headers = {
            "Truora-API-Key": self.TRUORA_APIKEY
        }
        
        url = self.url + "/" + validation_id
        
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            
            data = response.json()
            validation_status = data["validation_status"]
            print("nice validation, status: ", validation_status)
            return validation_status
        
        else:
            print(f"Error {response.status_code}")
            return False
        
    def check_validation_status(self, validation_id):
        max_wait_time = 15  # Tiempo máximo de espera en segundos
        elapsed_time = 0  # Tiempo transcurrido
        
        while elapsed_time < max_wait_time:
            # Llamada a la función que consulta la API
            validation_status = self.getValidation(validation_id)
            
            if validation_status:
                # Si el estado ya no es "pending", salir del bucle
                if validation_status != "pending":
                    return validation_status
            
            # Esperar 1 segundo antes de volver a consultar
            time.sleep(1)
            elapsed_time += 1
        
        # Si se alcanza el tiempo máximo, devolver "pending"
        return "pending"