import json
from flask import Blueprint, request, jsonify
from app.services.llm_service import LLMService

info_bp = Blueprint('info', __name__, url_prefix='/api')


@info_bp.route('/tags', methods=['GET'])
def get_tags():
    llm_service = LLMService()
    models = llm_service.get_models()    
    return jsonify({"models": models})

@info_bp.route('/version', methods=['GET'])
def get_version():

    with open('./project.json', 'r') as file:
        config = json.load(file)
    return jsonify({"version": config['version']})