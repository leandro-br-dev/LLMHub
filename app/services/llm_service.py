# app/services/llm_service.py
import json
import uuid
from app.services.ollama_service import OllamaService
from app.services.openai_service import OpenAIService
from app.services.anthropic_service import AnthropicService
from app.services.google_service import GoogleService

class LLMService:
    def __init__(self):
        self.llm_config = self.load_services_from_json('config_models.json')

    def load_services_from_json(self, file_path):
        with open(file_path, 'r') as file:
            config = json.load(file)

        return config['llm_services'] 

    def get_models(self):
        models = []
        for llm in self.llm_config:
            
            model = llm['model']
            if not ':' in str(model):
                model = model + ':latest'

            models.append(
                {
                    "name": model,
                    "model": model,
                    "digest": uuid.uuid4()
                }
            )        

        return models

    def get_llm_service(self, model):

        for llm in self.llm_config:
            if model == llm['model']:
                return llm['service']

        return None

    def select_model(self, model):
        model = str(model).replace(':latest', '')
        llm_service = self.get_llm_service(model)
        if llm_service:
            service_instance = globals()[llm_service + 'Service'](model)
            return service_instance     
        else:
            return None