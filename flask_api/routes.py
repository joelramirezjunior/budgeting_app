# routes.py
from flask import jsonify, request, Response
import uuid
import hashlib  # Import hashlib for hashing
from models import TransactionSchema, AccountSchema, FinanceSchema
from app.app import app, mongo
from statuscodes import ApiResponseStatus
from utils import generate_response

app.logger.setLevel("INFO")

@app.before_request
def log_request_info():
    # Here you can specify what you want to log.
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.get_data())

    if request.method == 'OPTIONS':
        return generate_response()

from flask import jsonify, request
from pymongo import ReturnDocument

@app.route('/add_transaction', methods=['POST', 'OPTIONS'])
def add_transaction():

    app.logger.info('%s Request made successfully', request)

    schema = TransactionSchema()
    accounts = mongo.db.accounts
    transactions = mongo.db.transactions

    json_data = request.get_json()

    transaction = json_data.get("transaction")

    if transaction is None: 
        app.logger.info("Transaction not sent in request. Cannot fulfill request.")
        response = generate_response({'status': ApiResponseStatus.INVALID_DATA, "message": "Invalid data, financial details not sent in correct format or missing contents."}, 400)
        return response
    
    try:
        schema.validate(transaction)
    except:
        app.logger.info(f'Invalid format of data: {transaction}')
        response = generate_response({'status': ApiResponseStatus.INVALID_DATA, "message": "Invalid data, financial details not sent in correct format or missing contents."}, 400)
        return response
    
    account_id = transaction.get("account_id");
    account = accounts.find_one({"account_id": account_id})

    if account is None:
        app.logger.info(f'No user found with id: {account_id)}')
        response = generate_response({'status': ApiResponseStatus.INVALID_DATA, "message": f"Invalid data, user with account_id {account_id} not found."}, 400)
        return response
    
    # Insert into the database
    transaction_id = transactions.insert_one(json_data).inserted_id

    # Update the user's transaction history
    updated_account = accounts.find_one_and_update(
        {'account_id': json_data['account_id']},
        {'$push': {'transactions': transaction_id}},  # Append the new transaction_id to the transactions list
        return_document=ReturnDocument.AFTER
    )
    
    if updated_account is None:
        app.logger.error("Failed to update account with new transaction")
        response = generate_response({'status': ApiResponseStatus.UPDATE_UNSUCCESFUL, "message": "Failed to update account with new transaction"}, 500)
        return response
    
    response = generate_response({'status': ApiResponseStatus.SUCCESS, 'transaction_id': str(transaction_id)}, 200)
    return response

@app.route('/add_financial_info', methods=['POST', 'OPTIONS'])
def add_financial_info():

    app.logger.info('%s Request made successfully', request)

    schema = FinanceSchema()
    json_data = request.get_json()
    finances = mongo.db.finances
    accounts = mongo.db.accounts

    finance_data = json_data.get("finance_data")
    if finance_data is None: 
        app.logger.ingo("Finance data sent in request is None. Submit a request with this value supplied")
    
    try:
        schema.validate(finance_data)
    except:
        app.logger.info(f'Invalid format of data: {finance_data}')
        response = generate_response({'status': ApiResponseStatus.INVALID_DATA, "message": "Invalid data, financial details not sent in correct format or missing contents."}, 400)
        return response
        
    account_id = finance_data.get("account_id")
    account = accounts.find_one({"account_id": account_id})

    if account is None:
        app.logger.info(f'No user found with account id: {account_id}')
        response = generate_response({'status': ApiResponseStatus.INVALID_DATA, "message": f"Invalid data, account_id {account_id} not found."}, 400)
        return response
    
    # Insert into the database
    finance_id = finances.insert_one(finance_data).inserted_id
    updated_account = accounts.find_one_and_update(
        {'account_id': account_id},
        {'$push': {'finances': finance_id}},  # Append the new transaction_id to the transactions list
        return_document=ReturnDocument.AFTER
    )

    if updated_account is None:
        app.logger.error("Failed to update account with new transaction")
        response = generate_response({'status': ApiResponseStatus.UPDATE_UNSUCCESFUL, "message": "Failed to update account with new transaction"}, 500)
        return response
    
    response = generate_response(jsonify({'status': ApiResponseStatus.SUCCESS, 'transaction_id': str(finance_id)}), 200)    
    app.logger.info(f"Sending response add_account: {response.get_data(as_text=True)}")
    return response
    



@app.route('/add_account', methods=['POST', 'OPTIONS'])
def add_account():
    print("/add_account Received Request: ", request)

    json_data = request.get_json()
    schema = AccountSchema()

    # Validate incoming data
    try:
        data = schema.load(json_data)
    except:
        response = generate_response(jsonify({'status': ApiResponseStatus.INVALID_DATA, "message": "Invalid data, incorrect parameters sent."}), 400)
        app.logger.info(f"Sending response add_account: {response.get_data(as_text=True)}")
        return response

    # Hash username and check for its existence
    hashed_username = hashlib.sha256(data['user_name'].encode()).hexdigest()
    accounts = mongo.db.accounts
    existing_account = accounts.find_one({"user_name": hashed_username})

    if existing_account is not None:
        response = generate_response(jsonify({"status": ApiResponseStatus.USERNAME_EXISTS, "message": "Username already exists"}), 200)
        app.logger.info(f"Sending response add_account: {response.get_data(as_text=True)}")
        return response

    # Generate a UUID for the account_id field
    # We will not generate this again for any user/ 
    # In the future add support for session keys.
    data['account_id'] = str(uuid.uuid4())

    # Hash other sensitive information
    hashed_first_name = hashlib.sha256(data['first_name'].encode()).hexdigest()
    hashed_last_name = hashlib.sha256(data['last_name'].encode()).hexdigest()

    #I know this is not secure, will use bcrypt later.
    hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()

   
    # Replace the original fields with hashed values
    data['first_name'] = hashed_first_name
    data['last_name'] = hashed_last_name
    data['password'] = hashed_password
    data['user_name'] = hashed_username

    accounts.insert_one(data).inserted_id
    # Return serialized data
    response = generate_response(jsonify({'status': ApiResponseStatus.SUCCESS, 'account_id': data['account_id']}, 200))
    app.logger.info(f"Sending response add_account: {response.get_data(as_text=True)}")
    return response


@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    print("/login Received Request: ", request)
    
    data = request.get_json()

    # Hash username and check for its existence
    hashed_username = hashlib.sha256(data['user_name'].encode()).hexdigest()
    accounts = mongo.db.accounts
    existing_account = accounts.find_one({"user_name": hashed_username})

    if existing_account is None:
        app.logger.info(f"Username not found: {data['user_name']}")
        response = generate_response(jsonify({'status': ApiResponseStatus.USERNAME_NOT_FOUND, "message": "Username does not exist"}), 400)
        return response

    # Hash other sensitive information
    # todo, use bcrypt
    hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
        
    if hashed_password != existing_account.password:
        response = generate_response(jsonify({'status': ApiResponseStatus.WRONG_PASSWORD, "message": "Password is incorrect"}), 400)
        app.logger.info(f"Sending response add_account: {response.get_data(as_text=True)}")
        return response


    # Return back their unique identifier / maybe should be session token later? 
    # Unique for each person?
    
    # Return serialized data
    response = generate_response(jsonify({'status': ApiResponseStatus.SUCCESS, 'account_id': str(existing_account.account_id)}), 200)
    app.logger.info(f"Sending response add_account: {response.get_data(as_text=True)}")
    return response