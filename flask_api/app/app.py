from flask import Flask
from flask_pymongo import PyMongo
from mongoengine import connect

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/budgeting_app'

mongo = PyMongo(app)

connect(host=app.config['MONGO_URI'])

import routes

