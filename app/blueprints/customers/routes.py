from app.blueprints.customers import customers_bp
from app.blueprints.customers.schemas import customer_schema, customers_schema, login_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Customer, db
from sqlalchemy import select, delete
from app.extension import limiter
from app.utils.utils import encode_token, token_required

@customers_bp.route("/login", methods = ["POST"])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return  jsonify(e.messages), 400
    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalars().first()
    
    if customer and customer.password  ==  password:
        token = encode_token(customer.id)
        
        response ={
            'status': 'success',
            'message': 'sucessfully logged in',
            'token': token
        }
        
        return jsonify(response), 200
    else:
        return jsonify({"message" : "Invalid email or password"})
    
    
@customers_bp.route("/", methods=['GET'])
def get_customers():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Customer)
        customers =  db.paginate(query, page=page, per_page=per_page)
        return customers_schema.jsonify(customers), 200
    except:
        query = select(Customer)
        customers = db.session.execute(query).scalars().all()
        return customers_schema.jsonify(customers), 200
    
    
    
    

@customers_bp.route("/", methods=["POST"])
@limiter.limit("10 per hour")
# it is important to add a limit here because there should be no reason to add more than 10 customers an hour to a server. I can understand busy days, but i don't more than 10 really.
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
        print(customer_data)
        
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'], password=customer_data['password'])
    db.session.add(new_customer)
    db.session.commit()
    
    return customer_schema.jsonify(new_customer), 200

@customers_bp.route("/", methods=["PUT"])
@token_required
def update_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()
    print(customer)
    
    if customer == None:
        return jsonify({"message": "invalid customer id"})
    
    try:
        customer_data = customer_schema.load(request.json)
        print(customer_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in customer_data.items():
        setattr(customer, field, value)
        
    db.session.commit()
    return customer_schema.jsonify(customer), 200

@customers_bp.route("/", methods=["DELETE"])
@token_required
def delete_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"successfully deleted customer {customer_id}"})
    