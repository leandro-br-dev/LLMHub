# app/__init__.py
import os
from flask import Flask
from config.config import DevelopmentConfig
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    load_dotenv()

    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(ProductionConfig)
    elif env == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    
    from app.controllers.info_controller import info_bp
    from app.controllers.chat_controller import chat_bp
    from app.controllers.chat_completions_controller import completions_bp
    from app.controllers.generate_controller import generate_bp
    app.register_blueprint(info_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(completions_bp)
    app.register_blueprint(generate_bp)
    
    return app
