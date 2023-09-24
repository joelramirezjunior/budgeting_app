# API Routes README

### note: in the works!

## Overview
This README is a guide for understanding the `routes.py` file in the project. The API routes are built using Flask and MongoDB and primarily focus on two types of resources: Transactions and Accounts. The two main routes are `/add_transaction` and `/add_account`.

## Requirements
- Flask
- MongoDB
- Python Libraries: `uuid`, `hashlib`, `jsonify`, `request`

## Models
Two models are defined in the script and are validated using Schemas (`TransactionSchema`, `AccountSchema`).

## Routes

### POST `/add_transaction`
This route is used for adding a new transaction record to the database.

#### Request Payload
JSON Object with the following fields:
- `amount`
- `date`
- `transaction_type`
- ...

#### Validation
The route uses the `TransactionSchema` to validate incoming data. If the data does not meet the schema's requirements, it returns a `400 Bad Request` status with the message "Invalid data".

#### Response
After successful insertion into the MongoDB transactions collection, the route returns a JSON object containing the transaction ID and the serialized data of the transaction.

#### Example Response
```json
{
  "transaction_id": "some_uuid",
  "transaction": { "amount": 100, "date": "2022-10-10", "transaction_type": "debit", ... }
}
```

### POST `/add_account`
This route is used for adding a new account record to the database.

#### Request Payload
JSON Object with the following fields:
- `first_name`
- `last_name`
- `email`
- `user_name`
- ...

Note: An `account_id` is automatically generated using `uuid`.

#### Validation
The route uses the `AccountSchema` to validate incoming data. Similar to `/add_transaction`, if the data doesn't meet the schema's requirements, a `400 Bad Request` status is returned with the message "Invalid data".

#### Data Hashing
Sensitive information like the `first_name`, `last_name`, `email`, and `user_name` are hashed using SHA-256 before being stored in the database.

#### Response
After successful insertion into the MongoDB accounts collection, the route returns a JSON object containing the account ID and the serialized (hashed) data of the account.

#### Example Response
```json
{
  "account_id": "some_uuid",
  "account": { "first_name": "hashed_value", "last_name": "hashed_value", "email": "hashed_value", "user_name": "hashed_value", ... }
}
```

## Error Handling
Both routes have basic error handling to check the validation of the incoming request data. If the data is invalid, a `400 Bad Request` status is returned along with an "Invalid data" message.

That's a brief overview of how the routes work. Feel free to dive into the code for a deeper understanding.