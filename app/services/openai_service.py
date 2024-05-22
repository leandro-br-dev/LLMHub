import os
import json
import openai
from datetime import datetime, timezone

class OpenAIService:

    def __init__(self, model):
        self.client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def format_messages(self, messages):

        messages_formatted = []
        for message in messages:
            
            message_formatted = {
                "role": message['role'],
                "content": [ 
                    {
                        "type": "text",
                        "text": message['content']
                    },
                ]
            }

            if message.get('images', False):                    
                for image in message['images']:
                    message_formatted['content'].append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image}"
                        }
                    })    
            
            messages_formatted.append(message_formatted)
        
        return messages_formatted

    def chat(self, messages = [], options = {}):                
        try:

            messages_formatted = self.format_messages(messages)            
            
            config = {
                "model": self.model,         
                "messages": messages_formatted,
                "stream": options.get("stream", False),
                "max_tokens": options.get("max_tokens", 1000),
                "format": { "type": options.get("format", "text") }
            }   

            response = self.client.chat.completions.create(
                model=config["model"],
                max_tokens=config["max_tokens"],
                messages=config["messages"],
                response_format=config["format"],
                stream=config["stream"]
            )

            if config["stream"] is True:

                def stream_content(response):

                    for chunk in response:                    
                        if chunk.choices[0].finish_reason != "stop":                       
                            yield json.dumps({
                                "model": chunk.model,
                                "created_at": datetime.utcfromtimestamp(chunk.created).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                                "message": {
                                    "role": "assistant",
                                    "content": chunk.choices[0].delta.content
                                },
                                "done": False
                            }) + '\n'
                        else:
                            yield json.dumps({
                                "model": chunk.model,
                                "created_at": datetime.utcfromtimestamp(chunk.created).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                                "message": {
                                    "role": "assistant",
                                    "content": ""
                                },
                                "done": True,
                            })  


                return stream_content(response)
            else:
                return json.dumps({
                    "model": response.model,
                    "created_at": datetime.utcfromtimestamp(response.created).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "message": {
                        "role": "assistant",
                        "content": response.choices[0].message.content
                    },           
                    "done": True,                
                })    

        except Exception as e:            
            return f"Error communicating with OpenaiService: {str(e)}"

    def completions(self, messages = [], options = {}):                
        try:

            messages_formatted = self.format_messages(messages)

            config = {
                "model": self.model,         
                "messages": messages_formatted,
                "stream": options.get("stream", False),
                "max_tokens": options.get("max_tokens", 1000),
                "format": { "type": options.get("format", "text") }
            }   

            response = self.client.chat.completions.create(
                model=config["model"],
                max_tokens=config["max_tokens"],
                messages=config["messages"],
                response_format=config["format"],
                stream=config["stream"]
            )

            if config["stream"] is True:
                def stream_content(response):
                    for chunk in response:                    
                        if chunk.choices[0].finish_reason != "stop":  
                            chunk.created = datetime.utcfromtimestamp(chunk.created).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                            yield chunk.json() + '\n'
                        else:
                            chunk.created = datetime.utcfromtimestamp(chunk.created).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                            yield chunk.json()

                return stream_content(response)
            else:

                response.created = datetime.utcfromtimestamp(response.created).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

                return response.json()
                

        except Exception as e:            
            return f"Error communicating with OpenaiService: {str(e)}"

