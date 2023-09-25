from flask import Flask
from flask_pymongo import PyMongo
from mongoengine import connect
from flask_cors import CORS, cross_origin
import json


app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "http://127.0.0.1:3000"}})


app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/budgeting_app'
mongo = PyMongo(app)

connect(host=app.config['MONGO_URI'])

# routes.py
from flask import jsonify, request, make_response, Response
import uuid
import hashlib  # Import hashlib for hashing
from models import TransactionSchema, AccountSchema

app.logger.setLevel("INFO")

@app.before_request
def log_request_info():
    # Here you can specify what you want to log.
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.get_data())
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

@app.route('/')
def index():
    return 'Welcome to your Flask application!'

@app.route('/add_transaction', methods=['POST', 'OPTIONS'])
def add_transaction():

    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response
    
    app.logger.info('%s Request made successfully', request)
    schema = TransactionSchema()
    transactions = mongo.db.transactions
    json_data = request.get_json()
    
    # Validate incoming data
    try:
        data = schema.load(json_data)
    except:
        app.logger.info(f'Invalid format of data: {json_data}')
        return jsonify({"message": "Invalid data"}), 400

    # Insert into the database
    transaction_id = transactions.insert_one(data).inserted_id

    # Return serialized data
    result = schema.dump(data)
    return jsonify({'transaction_id': str(transaction_id), 'transaction': result})

@app.route('/add_financial_info', methods=['POST', 'OPTIONS'])
def add_financial_info():

    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response
    
    app.logger.info('%s Request made successfully', request)
    schema = TransactionSchema()
    transactions = mongo.db.transactions
    json_data = request.get_json()
    
    # Validate incoming data
    try:
        data = schema.load(json_data)
    except:
        app.logger.info(f'Invalid format of data: {json_data}')
        return jsonify({"message": "Invalid data"}), 400

    # Insert into the database
    transaction_id = transactions.insert_one(data).inserted_id

    # Return serialized data
    result = schema.dump(data)
    return jsonify({'transaction_id': str(transaction_id), 'transaction': result})



@app.route('/add_account', methods=['POST', 'OPTIONS'])
def add_account():
    print("/add_account Received Request: ", request)
    response = make_response()
    if request.method == 'OPTIONS':
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response
    schema = AccountSchema()
    accounts = mongo.db.accounts
    json_data = request.get_json()

    # Generate a UUID for the account_id field
    json_data['account_id'] = str(uuid.uuid4())

    # Validate incoming data
    try:
        data = schema.load(json_data)
    except:
        return jsonify({"message": "Invalid data"}), 400

    # Hash sensitive information
    hashed_first_name = hashlib.sha256(data['first_name'].encode()).hexdigest()
    hashed_last_name = hashlib.sha256(data['last_name'].encode()).hexdigest()
    hashed_email = hashlib.sha256(data['email'].encode()).hexdigest()
    hashed_username =  hashlib.sha256(data['user_name'].encode()).hexdigest()
    # Replace the original fields with hashed values
    data['first_name'] = hashed_first_name
    data['last_name'] = hashed_last_name
    data['email'] = hashed_email
    data['user_name'] = hashed_username
    
    print(data['user_name'])

    # Insert into the database
    account_id = accounts.insert_one(data).inserted_id

    # Return serialized data
    result = schema.dump(data)

    response = make_response(jsonify({'account_id': str(account_id), 'account': result}), 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")

    return response


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000, debug=True)


