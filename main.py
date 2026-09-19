from flask import Flask
from flask_cors import CORS
from api.services import bp as service_bp
import os


app = Flask(__name__)
CORS(app,origins=os.getenv("frontend_url"))


app.register_blueprint(service_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)