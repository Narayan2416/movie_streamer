from flask import Flask, Response, render_template, request,Blueprint
from apis.services import bp as service_bp
from db.moviesDb import getMovies
import os

app = Flask(__name__)


app.register_blueprint(service_bp, url_prefix="/api")

@app.route("/")
def index():
    movies=getMovies()
    print(movies,"it has somrthing?")
    return render_template("home.html", movies=movies)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)