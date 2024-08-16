from flask import Blueprint, request, current_app
from flask import jsonify


main = Blueprint("api_status_blueprint", __name__)

@main.route('/', methods=['GET'])
def status():
    return jsonify("api working")

