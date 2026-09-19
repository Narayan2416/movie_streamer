from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["movies_streamer"]
collection = db["movies"]

def getMovieIds():
    return list(collection.find({}, {"_id": 1}))

def getMovieById(movie_id):
    return collection.find_one({"_id": movie_id})
