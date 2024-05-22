import json
import os
import google.generativeai as genai
from datetime import datetime, timezone

class GoogleService:

    def __init__(self, model):
        self.client = genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = model

    def format_messages(self, messages):

        formatted_messages = []

        for message in messages:

            role = "model" if message['role'] == "assistant" else message['role']
            if role == 'system':
                formatted_messages.append(
                    {
                        "parts": [
                            {"text": message['content']},
                        ],
                        "role": "user",
                    }
                )
                formatted_messages.append(
                    {
                        "parts": [
                            {"text": "OK!"},
                        ],
                        "role": "model",
                    }
                )
            else:
                formatted_messages.append(
                    {
                        "parts": [
                            {"text": message['content']},
                        ],
                        "role": role,
                    }
                )

        return formatted_messages

    def chat(self, messages = [], options = {}):                
        try:

            messages_formatted = self.format_messages(messages)     

            safety_settings = {
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
            }

            config = {
                "max_output_tokens": options.get("max_tokens", 2048 * 2),
                "temperature": 0.7,
                "top_p": 1,
                "top_k": 1,
                "candidate_count": 1,              
            }            

            session = genai.GenerativeModel(
                self.model, generation_config=config, safety_settings=safety_settings
            )
            
            chat = session.start_chat(history=messages_formatted[0:-1])            
            response = chat.send_message(messages_formatted[-1], stream=options.get("stream", False))            

            if options.get("stream", False) is True:

                def stream_content(response):
                    
                    for chunk in response:    
       
                        now_utc = datetime.now(timezone.utc)    
                           
                        yield json.dumps({
                            "model": self.model,
                            "created_at": now_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                            "message": {
                                "role": "assistant",
                                "content": chunk.candidates[0].content.parts[0].text
                            },
                            "done": False
                        }) + '\n'

                    now_utc = datetime.now(timezone.utc)    

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
                return json.dumps({
                    "model": self.model,
                    "created_at":  now_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "message": {
                        "role": "assistant",
                        "content": response.text
                    },           
                    "done": True,                
                })    

        except Exception as e:            
            return f"Error communicating with GoogleAiService: {str(e)}"

    def completions(self, messages = [], options = {}):                
        try:

            messages_formatted = self.format_messages(messages)      

            safety_settings = {
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
            }

            config = {
                "max_output_tokens": options.get("max_tokens", 2048 * 2),
                "temperature": 0.7,
                "top_p": 1,
                "top_k": 1,
                "candidate_count": 1,              
            }            

            session = genai.GenerativeModel(
                self.model, generation_config=config, safety_settings=safety_settings
            )
            
            chat = session.start_chat(history=messages_formatted[0:-1])            
            response = chat.send_message(messages_formatted[-1], stream=options.get("stream", False))            

            if options.get("stream", False) is True:

                def stream_content(response):
                    
                    for chunk in response:    
       
                        now_utc = datetime.now(timezone.utc)    
                           
                        yield json.dumps({
                            "choices": [
                                {      
                                    "index": 0,
                                    "logprobs": None,
                                    "message": {
                                        "content": chunk.candidates[0].content.parts[0].text,
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

                    now_utc = datetime.now(timezone.utc)    

                    yield json.dumps({
                        "choices": [
                            {      
                                "index": 0,
                                "logprobs": None,
                                "message": {
                                    "content": "",
                                    "role": "assistant",
                                    "function_call": None,
                                    "tool_calls": None
                                }
                            }
                        ],
                        "created": now_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "done": True,
                    }) 

                return stream_content(response)
            else:
                now_utc = datetime.now(timezone.utc)
                return json.dumps({
                    "choices": [
                        {      
                            "index": 0,
                            "logprobs": None,
                            "message": {
                                "content": response.text,
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

        except Exception as e:            
            return f"Error communicating with GoogleAiService: {str(e)}"


