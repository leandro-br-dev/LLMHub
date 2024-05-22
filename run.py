# run.py
import os
from app import create_app

if __name__ == "__main__":
    app = create_app()
    port = os.getenv('FLASK_RUN_PORT', 5000)
    app.run(port=port)
