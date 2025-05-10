from app.models import Customer
from app.extension import ma
from marshmallow import Schema, fields

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

login_schema = LoginSchema()
