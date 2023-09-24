from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"

mongo = PyMongo(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    transactions = mongo.db.transactions
    # Parse transaction details from request
    user_id = request.json.get('user_id')
    category = request.json.get('category')
    amount = request.json.get('amount')
    date = request.json.get('date')
    description = request.json.get('description')
    
    # Insert to the database
    transaction_id = transactions.insert({
        'user_id': user_id,
        'category': category,
        'amount': amount,
        'date': date,
        'description': description
    })
    
    return jsonify({'transaction_id': str(transaction_id)})


app.run(port=5000)