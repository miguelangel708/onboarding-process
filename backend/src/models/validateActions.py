from dataclasses import dataclass
import requests
import os
from dotenv import load_dotenv
import time


class validateActions:

    validation_status: str
    validation_id: str
    processing_time: str
    validation_date: str

    def __init__(self, document_validation, country, document_type, user_authorized):
        
        load_dotenv()
        self.TRUORA_APIKEY = os.environ.get("truoraApiKey", "")
        self.url = os.environ.get("truoraDocumentValidationURL", "")

        self.document_validation = document_validation
        self.country = country
        self.document_type = document_type
        self.user_authorized = user_authorized

    def pipeline_document_validation(self):
        # 1. get the initial validation and thus acquire the front_url and back_url
        data = self.createValidation()
        # 2. extract links for uploading
        front_url = data["instructions"]["front_url"]
        reverse_url = data["instructions"]["reverse_url"]
        # upload del front
        validate_front_upload = self.uploadDocFrontPicture(front_url)
        # upload reverse
        validate_reverse_upload = self.uploadDocReversePicture(reverse_url)
        # validate the uploads
        if not (validate_front_upload and validate_reverse_upload):
            return "fail loading images in the pipeline", 400
        # extract the id for validation
        self.validation_id = data["validation_id"]
        # get validation
        self.check_validation_status()

    def createValidation(self):

        headers = {
            "Truora-API-Key": self.TRUORA_APIKEY,
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Parameters for filtering data in a GET request
        params = {
            "type": "document-validation",
            "country": self.country,
            "document_type": self.document_type,
            "user_authorized": self.user_authorized,
        }

        response = requests.post(self.url, headers=headers, data=params)

        if response.status_code == 200:
            data = response.json()
            print("account id validation response: ", data["account_id"])
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
            response = requests.put(
                front_url, headers=headers, data=image_file)

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
            response = requests.put(
                reverse_url, headers=headers, data=image_file)

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
            validation_date = data["creation_date"]
            print("nice validation, status: ", validation_status)
            return validation_status, validation_date

        else:
            print(f"Error {response.status_code}")
            return False

    def check_validation_status(self):
        max_wait_time = 30  # Maximum waiting time in seconds
        elapsed_time = 0  # Time elapsed

        while elapsed_time < max_wait_time:
            # Time elapsed
            validation_status, validation_date = self.getValidation(
                self.validation_id)

            if validation_status:
                # If the status is no longer “pending”, exit the loop.
                if validation_status != "pending":
                    self.validation_status = validation_status
                    self.processing_time = elapsed_time
                    self.validation_date = validation_date
                    return

            # Wait 1 second before consulting again.
            time.sleep(1)
            elapsed_time += 1

        # Wait 1 second before consulting again.
        self.validation_status = "pending"
        self.processing_time = elapsed_time
        self.validation_date = validation_date
