from flask import Blueprint, request, jsonify, Response
from app.services.llm_service import LLMService
from app.services.ollama_service import OllamaService
import json
chat_bp = Blueprint('chat', __name__, url_prefix='/api')

@chat_bp.route('/chat', methods=['POST'])
def chat(): 

    try:        
        data = json.loads(request.data)

        if not data:
            return jsonify({'error': 'Invalid JSON or empty request body'}), 400

        model = data.get('model')
        messages = data.get('messages')
        options = data.get('options', {})    
        options['stream'] = options.get('stream', True)

        if len(messages) <= 0 or not model:
            return jsonify({'message': 'Missing data'}), 400
        
        llm_service = LLMService()
        llm_model = llm_service.select_model(model)

        if llm_model is not None:
            if options['stream'] is True :            
                return Response(llm_model.chat(messages, options), content_type='application/x-ndjson')
            else: 
                return Response(llm_model.chat(messages, options), content_type='application/json') 
        else:
            return jsonify({'message': 'Model not found'}), 400

    except Exception as e:
        print('Error: ', e)