from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient
from mongoengine import connect
from flask_cors import CORS, cross_origin
import json


app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "http://127.0.0.1:3000"}})


app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/budgeting_app'
mongo = PyMongo(app)

# Function to drop all collections in the database
# def drop_all_collections():
#     client = MongoClient('mongodb://127.0.0.1:27017/')
#     db = client['budgeting_app']
#     for collection_name in db.list_collection_names():
#         db[collection_name].drop()

# Drop all collections at the start of the app
# drop_all_collections()

connect(host=app.config['MONGO_URI'])

import routes

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000, debug=True)
