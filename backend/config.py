import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    DEBUG = True
    PORT = 5000
    UPLOADS_PATH = "src/uploads"
    TRUORA_APIKEY = os.environ.get("truoraApiKey", "")


