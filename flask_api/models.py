from marshmallow import Schema, fields

class TransactionSchema(Schema):
    _id = fields.Str(required=True)
    user_id = fields.Str(required=True)
    type = fields.Str(required=True)
    category = fields.Str(required=True)
    amount = fields.Float(required=True)
    date = fields.DateTime(required=True)
    description = fields.Str()



class AccountSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    user_name = fields.Str(required=True)
    account_id = fields.Str(required=True)
    email = fields.Email(required=True)
    retirement_amount = fields.Float(required=False)
    savings = fields.Float(required=False)
    checkings = fields.Float(required=False)
