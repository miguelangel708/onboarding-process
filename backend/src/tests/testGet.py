import requests
import os 
from dotenv import load_dotenv

load_dotenv()
TRUORA_APIKEY = os.environ.get("truoraApiKey", "")


url = "https://api.validations.truora.com/v1/validations"


# Headers adicionales
headers = {
    "Truora-API-Key": TRUORA_APIKEY,
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

response = requests.post(url, headers=headers, data=params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error {response.status_code}")
