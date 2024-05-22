import anthropic
import base64
import json
import magic
import os
from datetime import datetime, timezone

class AnthropicService:

    def __init__(self, model):
        self.client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = model
        self.magic = magic.Magic(mime=True)

    def format_messages(self, messages):
       
        messages_formatted = []
        for message in messages:

            if message['content'] == "":
                continue
            
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
                    
                    image_in_bytes = base64.b64decode(image)                    
                    image_type = self.magic.from_buffer(image_in_bytes)                    
                    message_formatted['content'].append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": f"{image_type}",
                            "data": image,
                        }
                    })    
            
            messages_formatted.append(message_formatted)
        
        return messages_formatted

    def chat(self, messages = [], options = {}):
        
        try:
            
            system = None
            for message in messages[:]:
                if message['role'] == 'system':
                    system = message['content']
                    messages.remove(message)

            messages_formatted = self.format_messages(messages)

            config = {
                "model": self.model,              
                "stream": options.get("stream", False),
                "messages": messages_formatted,
                "max_tokens": options.get("max_tokens", 1000),
                "format": { "type": options.get("format", "text") }
            }

            if system:
                config['system'] = system
       
            response = self.client.messages.create(
                model=config["model"],
                system=config.get("system", ""),                  
                messages=config["messages"],    
                max_tokens=config["max_tokens"],  
                stream=config["stream"],          
            )
            
            if config["stream"] is True:

                def stream_content(response):                
                    for chunk in response:    
                        now_utc = datetime.now(timezone.utc)
                        
                        if chunk.type == "content_block_delta":
                            yield json.dumps({
                                "model": self.model,
                                "created_at": now_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                                "message": {
                                    "role": "assistant",
                                    "content": chunk.delta.text
                                },
                                "done": False
                            }) + '\n'
                        elif chunk.type == "message_stop":                          
                            yield json.dumps({
                                "model": self.model,
                                "created_at": now_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                                "message": {
                                    "role": "assistant",
                                    "content": ""
                                },
                                "done": True,
                            })            

                return stream_content(response)
            
            else:                

                now_utc = datetime.now(timezone.utc)
                return json.dumps( {
                        "model": self.model,
                        "created_at": now_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "message": {
                            "role": "assistant",
                            "content": response.content[0].text
                        },           
                        "done": True,                
                    }
                )                

        except Exception as e:
            return f"Error communicating with AnthropicService: {str(e)}"

    def completions(self, messages = [], options = {}):
        
        try:

            system = None
            for message in messages[:]:
                if message['role'] == 'system':
                    system = message['content']
                    messages.remove(message)

            config = {
                "model": self.model,              
                "stream": options.get("stream", False),
                "messages": messages,
                "max_tokens": options.get("max_tokens", 1000),
                "format": { "type": options.get("format", "text") }
            }

            if system:
                config['system'] = system
       
            response = self.client.messages.create(
                model=config["model"],    
                system=config.get("system", ""),     
                messages=config["messages"],    
                max_tokens=config["max_tokens"],  
                stream=config["stream"],          
            )

            if config["stream"] is True:

                def stream_content(response):                
                    for chunk in response:    
                        now_utc = datetime.now(timezone.utc)
                        if chunk.type == "content_block_delta":                            
                            yield json.dumps({
                                    "choices": [
                                        {      
                                            "index": 0,
                                            "logprobs": None,
                                            "message": {
                                                "content": chunk.delta.text,
                                                "role": "assistant",
                                                "function_call": None,
                                                "tool_calls": None
                                            }
                                        }
                                    ],
                                    "created": now_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                                    "model": self.model,
                                    "object": "chat.completion",
                                    "done": False                              
                                }) + '\n'
                        elif chunk.type == "message_stop":                          
                            yield json.dumps({
                                "choices": [
                                    {      
                                        "index": 0,
                                        "logprobs": None,
                                        "message": {
                                            "content": chunk.delta.text,
                                            "role": "assistant",
                                            "function_call": None,
                                            "tool_calls": None
                                        }
                                    }
                                ],
                                "created": now_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                                "model": self.model,
                                "object": "chat.completion",
                                "done": True,
                            })            

                return stream_content(response)
            
            else:               
      
                now_utc = datetime.now(timezone.utc)
                return json.dumps({
                        "id": response.id,
                        "choices": [
                            {
                                "finish_reason": response.stop_reason,
                                "index": 0,
                                "logprobs": None,
                                "message": {
                                    "content": response.content[0].text,
                                    "role": "assistant",
                                    "function_call": None,
                                    "tool_calls": None
                                }
                            }
                        ],
                        "created": now_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "model": response.model,
                        "object": "chat.completion",
                        "system_fingerprint": None,
                        "usage": {
                            "completion_tokens": response.usage.output_tokens,
                            "prompt_tokens": response.usage.input_tokens,
                            "total_tokens": int(response.usage.output_tokens) + int(response.usage.input_tokens)
                        }
                    })                

        except Exception as e:
            return f"Error communicating with AnthropicService: {str(e)}"

