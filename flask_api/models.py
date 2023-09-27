from marshmallow import Schema, fields

class TransactionSchema(Schema):
    _id = fields.Str(required=True)
    user_id = fields.Str(required=True)
    type = fields.Str(required=True)
    category = fields.Str(required=True)
    amount = fields.Float(required=True)
    date = fields.DateTime(required=True)
    description = fields.Str(required=False) 

class FinanceSchema(Schema):
    account_id = fields.Str(required=True)
    retirement_amount = fields.Float(required=False)
    savings = fields.Float(required=False)
    checkings = fields.Float(required=False)
    # will add support for auto loans in the future

class AccountSchema(Schema):
    account_id = fields.Str(required=False) 
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    user_name = fields.Str(required=True)
    password = fields.Str(required=True)
    transactions = fields.List(fields.Str(), required=False)  # New field to hold an array of transaction IDs
    finances = fields.List(fields.Str(), required=False)
