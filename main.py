from flask import Flask
from flask_cors import CORS
from api.services import bp as service_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
frontend_urls = os.getenv("frontend_url", "").split(",")

CORS(app, origins=frontend_urls)


app.register_blueprint(service_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)