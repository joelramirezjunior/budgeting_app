import unittest
from flask_testing import TestCase
import uuid
import hashlib  # Import hashlib for hashing
from app.app import app, mongo  # Replace mongo with mongo as that's what you've defined
from models import TransactionSchema, AccountSchema # Import the Transaction model from models.py
from bson import ObjectId
from datetime import datetime
import json 

class TransactionTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.app.config.from_object('config.TestingConfig')
        self.client = self.app.test_client
        self.mongo = mongo
        
        with self.app.app_context():
            self.mongo.db.transactions.delete_many({})

    def tearDown(self):
        with self.app.app_context():
            self.mongo.db.transactions.delete_many({})
        
    def test_add_transaction(self):
        schema = TransactionSchema()
        
        transaction_payload = {
            "_id": str(ObjectId()),
            "user_id": str(ObjectId()),
            "type": "Expense",
            "category": "Groceries/Food Staples",
            "amount": 50.00,
            "date": datetime.utcnow().isoformat(),
            "description": "Weekly grocery shopping"
        }
        
        # Validate and serialize payload data
        try:
            valid_payload = schema.load(transaction_payload)
    
        except:
            self.fail("The transaction payload is invalid.")

        # Save transaction to MongoDB
        with self.app.app_context():
            self.mongo.db.transactions.insert_one(valid_payload)
        
        # Query the transaction to see if it's been added correctly
        with self.app.app_context():
            saved_transaction = self.mongo.db.transactions.find_one({"_id": valid_payload["_id"]})
        
        # Validate the saved transaction
        if saved_transaction:
            self.assertEqual(saved_transaction['category'], "Groceries/Food Staples")
        else:
            self.fail("The transaction was not saved.")


class API_TEST_ADD(TestCase):

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        with app.app_context():
            mongo.db.transactions.delete_many({})

    def tearDown(self):
        with app.app_context():
            mongo.db.transactions.delete_many({})
  
    def test_add_transaction_API(self):
        schema = TransactionSchema()
        # Create a sample transaction payload
        transaction_payload = {
            "_id": str(ObjectId()),
            "user_id": str(ObjectId()),
            "type": "Expense",
            "category": "Groceries/Food Staples",
            "amount": 50.00,
            "date": datetime.utcnow().isoformat(),
            "description": "Weekly grocery shopping"
        }
        
         # Validate and serialize payload data
        try:
            valid_payload = schema.load(transaction_payload)
        except:
            self.fail("The transaction payload is invalid.")

        # Use Flask's test_client to send a POST request to the /add_transaction endpoint
        response = self.client.post(
            '/add_transaction',
            data=json.dumps(transaction_payload),
            content_type='application/json'
        )

        # Check if the request was successful
        self.assertEqual(response.status_code, 200, f"Expected 200 OK but got {response.status_code}. Response data: {response.data.decode()}")

        if response.status_code == 200:
            # Parse the JSON response
            response_data = json.loads(response.data.decode())
            
            # Validate the transaction ID exists in the response
            self.assertIn('transaction_id', response_data)

            with self.app.app_context():
                saved_transaction = mongo.db.transactions.find_one({"_id": response_data["transaction"]["_id"]})

        
            # Validate the saved transaction
            self.assertEqual(saved_transaction['category'], "Groceries/Food Staples")

class AccountTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        self.mongo = mongo
        with app.app_context():
            self.mongo.db.accounts.delete_many({})

    def tearDown(self):
        with app.app_context():
            self.mongo.db.accounts.delete_many({})

    def test_add_account(self):
        schema = AccountSchema()

        account_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "user_name": "johndoe",
            "account_id": str(uuid.uuid4()),  # Generate a UUID
            "email": "johndoe@example.com",
            "retirement_amount": 100000,
            "savings": 0,
            "checkings": 123451,
        }

        # Validate and serialize payload data
        try:
            valid_payload = schema.load(account_payload)
            print(valid_payload)
        except:
            self.fail("The transaction payload is invalid.")

        # Send a POST request to the /add_account endpoint
        response = self.client.post(
            '/add_account',
            json=account_payload
        )

        # Check if the request was successful (status code 200)
        self.assertEqual(response.status_code, 200)

        # Query the account to see if it's been added correctly

        print( hashlib.sha256(account_payload['user_name'].encode()).hexdigest())
        with app.app_context():
            saved_account = self.mongo.db.accounts.find_one({"user_name":  hashlib.sha256(account_payload['user_name'].encode()).hexdigest()})

        # Validate the saved account
        if saved_account:
            # Verify that sensitive information is hashed
            self.assertTrue(account_payload['first_name'] not in saved_account)
            self.assertTrue(account_payload['last_name'] not in saved_account)
            self.assertTrue(account_payload['email'] not in saved_account)

        else:
            self.fail("The account was not saved.")
