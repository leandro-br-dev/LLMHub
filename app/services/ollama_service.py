# app/services/ollama_service.py
import os
import json
import requests

class OllamaService:

    def __init__(self, model):
        self.model = model

    def _stream_content(self, response):
        for chunk in response:
            yield chunk

    def chat(self, messages = [], options = {}):

        try:

            print('entrou no chat ollama')

            config = {
                "model": self.model,            
                "messages": messages,
                "stream": options['stream']
            }        

            response = requests.post(os.getenv('OLLAMA_API') + "/api/chat", json=config, stream=config['stream'])
                
            if response.status_code == 200: 
                if options['stream'] is True:
                    return self._stream_content(response)                    
                else:                                 
                    return json.dumps(response.json())
            else:
                return "Erro ao enviar a mensagem para o OllamaService"

        except Exception as e:
            return f"Error communicating with OllamaService: {str(e)}"

    def completions(self, messages = [], options = {}):

        try:
            config = {
                "model": self.model,            
                "messages": messages,
                "stream": options['stream']
            }        
        
            response = requests.post(os.getenv('OLLAMA_API') + "/v1/chat/completions", json=config, stream=config['stream'])
            if response.status_code == 200: 
                if options['stream'] is True:                    
                    return self._stream_content(response)                    
                else:                                                     
                    return json.dumps(response.json())
            else:
                return "Erro ao enviar a mensagem para o OllamaService"
        except Exception as e:
            return f"Error communicating with OllamaService: {str(e)}"

    def generate(self, messages = [], options = {}):

        try:

            config = {
                "model": self.model,     
                "system": messages[0],     
                "prompt": messages[-1],
                "stream": options['stream']
            }        
        
            response = requests.post(os.getenv('OLLAMA_API') + "/api/generate", json=config, stream=config['stream'])
            if response.status_code == 200: 
                if options['stream'] == True:
                    return self._stream_content(response)                    
                else:                                                 
                    return json.dumps(response.json())
            else:
                return "Erro ao enviar a mensagem para o OllamaService"
        except Exception as e:
            return f"Error communicating with OllamaService: {str(e)}"
