from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["movie_streamer"]
collection = db["movies"]

def getMovies():
    return list(collection.find({}, {"id": 1,"movie_title": 1}))

def getMovieById(movie_id):
    return collection.find_one({"id": movie_id})
