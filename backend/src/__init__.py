from flask import Flask
from flask_cors import CORS
from config import Config
from .routes import apiStatus, generalApi

app = Flask(__name__)
CORS(app)

# inicializate database
app.app_context()
app.config.from_object(Config)


app.register_blueprint(apiStatus.main, url_prefix = '/')
app.register_blueprint(generalApi.main, url_prefix = '/api')

# app.register_blueprint(auth.main, url_prefix = '/auth')
