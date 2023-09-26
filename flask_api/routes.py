# routes.py
from flask import jsonify, request, make_response, Response
import uuid
import hashlib  # Import hashlib for hashing
from models import TransactionSchema, AccountSchema
from app.app import app, mongo

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
        app.logger.info(f"Sending response: {response.get_data(as_text=True)}")
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
        app.logger.info(f"Sending response Trans: {response.get_data(as_text=True)}")
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
    response = make_response(jsonify({'transaction_id': str(transaction_id), 'transaction': result}), 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

@app.route('/add_financial_info', methods=['POST', 'OPTIONS'])
def add_financial_info():

    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        app.logger.info(f"Sending response add_financial_info: {response.get_data(as_text=True)}")
        return response
    
    app.logger.info('%s Request made successfully', request)

    schema = TransactionSchema()
    transactions = mongo.db.transactions
    json_data = request.get_json()

    # Validate incoming data
    try:
        #We only require the user_id as a schema as a failsafe to make sure 
        #We only modify their data. Will later turn into session key.
        data = schema.load(json_data)
    except:
        app.logger.info(f'Invalid format of data: {json_data}')
        response = Response(jsonify({"message": "Invalid data, no ID recieved."}), 400)
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response


    # Insert into the database
    transaction_id = transactions.insert_one(data).inserted_id
    response = Response(jsonify({'transaction_id': str(transaction_id)}), 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    app.logger.info(f"Sending response add_account: {response.get_data(as_text=True)}")
    return response
    



@app.route('/add_account', methods=['POST', 'OPTIONS'])
def add_account():
    print("/add_account Received Request: ", request)
    response = make_response()

    if request.method == 'OPTIONS':
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        app.logger.info(f"Sending response add_account: {response.get_data(as_text=True)}")
        return response

    json_data = request.get_json()
    schema = AccountSchema()

    # Validate incoming data
    try:
        data = schema.load(json_data)
    except:
        response = make_response(jsonify({"message": "Invalid data"}), 400)
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        app.logger.info(f"Sending response add_account: {response.get_data(as_text=True)}")
        return response

    # Hash username and check for its existence
    hashed_username = hashlib.sha256(data['user_name'].encode()).hexdigest()

    accounts = mongo.db.accounts
    existing_account = accounts.find_one({"user_name": hashed_username})

    if existing_account is not None:
        response = make_response(jsonify({"message": "Username already exists"}), 200)
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        app.logger.info(f"Sending response add_account: {response.get_data(as_text=True)}")
        return response

    # Generate a UUID for the account_id field
    # We will not generate this again for any user/ 
    # In the future add support for session keys.
    json_data['account_id'] = str(uuid.uuid4())

    # Hash other sensitive information
    hashed_first_name = hashlib.sha256(data['first_name'].encode()).hexdigest()
    hashed_last_name = hashlib.sha256(data['last_name'].encode()).hexdigest()
    hashed_email = hashlib.sha256(data['email'].encode()).hexdigest()

    # Replace the original fields with hashed values
    data['first_name'] = hashed_first_name
    data['last_name'] = hashed_last_name
    data['email'] = hashed_email
    data['user_name'] = hashed_username


    # Return serialized data
    response = make_response(jsonify({'account_id': str(json_data['account_id'])}), 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    app.logger.info(f"Sending response add_account: {response.get_data(as_text=True)}")
    return response


@app.route('/login', methods=['POST', 'OPTIONS'])
def add_account():
    print("/login Received Request: ", request)
    response = make_response()

    if request.method == 'OPTIONS':
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        app.logger.info(f"Sending response add_account: {response.get_data(as_text=True)}")
        return response

    data = request.get_json()

    # No need to validate schema as it is just username and password

    # Hash username and check for its existence
    hashed_username = hashlib.sha256(data['user_name'].encode()).hexdigest()
    accounts = mongo.db.accounts
    existing_account = accounts.find_one({"user_name": hashed_username})

    if existing_account is None:
        print("User with that username does not exist")
        response = make_response(jsonify({"message": "Username does not exists"}), 201)
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        app.logger.info(f"Sending response add_account: {response.get_data(as_text=True)}")
        return response

    # Hash other sensitive information
    hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
    
    if hashed_password != existing_account.password:
        response = make_response(jsonify({"message": "Wrong password"}), 203)
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        app.logger.info(f"Sending response add_account: {response.get_data(as_text=True)}")
        return response


    # Return back their unique identifier / maybe should be session token later? 
    # Unique for each person?
    
    # Return serialized data
    response = make_response(jsonify({'account_id': str(existing_account.account_id)}), 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    app.logger.info(f"Sending response add_account: {response.get_data(as_text=True)}")
    return response