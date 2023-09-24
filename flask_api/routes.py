# routes.py
from app.app import app, mongo  # Replace 'your_project' with your actual project name
from flask import jsonify, request
import uuid
import hashlib  # Import hashlib for hashing
from models import TransactionSchema, AccountSchema

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    schema = TransactionSchema()
    transactions = mongo.db.transactions
    json_data = request.get_json()
    
    # Validate incoming data
    try:
        data = schema.load(json_data)
    except:
        return jsonify({"message": "Invalid data"}), 400

    # Insert into the database
    transaction_id = transactions.insert_one(data).inserted_id

    # Return serialized data
    result = schema.dump(data)
    return jsonify({'transaction_id': str(transaction_id), 'transaction': result})


@app.route('/add_account', methods=['POST'])
def add_account():
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
    return jsonify({'account_id': str(account_id), 'account': result})
