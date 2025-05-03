from app.blueprints.mechanics import mechanics_bp
from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Mechanic, db
from sqlalchemy import select, delete
from app.extension import cache

@mechanics_bp.route("/", methods=["POST"])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
        print(mechanic_data)
        
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_mechanic = Mechanic(name=mechanic_data['name'], email=mechanic_data['email'], phone=mechanic_data['phone'], salary=mechanic_data['salary'])
    db.session.add(new_mechanic)
    db.session.commit()
    
    return mechanic_schema.jsonify(new_mechanic), 200

@mechanics_bp.route("/", methods=['GET'])
@cache.cached(timeout=60)
# important to cache the get method here because to reduce the database query if a supervisor was looking to retreive info on a mechanic, and submitting frequent request.
def get_mechanics():
    query = select(Mechanic)
    result = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(result), 200

@mechanics_bp.route("<int:mechanic_id>", methods=["PUT"])
def update_mechanic(mechanic_id):
    query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()
    print(mechanic)
    
    if mechanic == None:
        return jsonify({"message": "invalid mechanic id"})
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
        print(mechanic_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in mechanic_data.items():
        setattr(mechanic, field, value)
        
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route("/<int:mechanic_id>", methods=["DELETE"])
def delete_mechanic(mechanic_id):
    query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"successfully deleted mechanic {mechanic_id}"})
    
@mechanics_bp.route("/most_tickets>", methods=["GET"])
def most_tickets_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    
    mechanics.sort(key = lambda mechanics : len(mechanics.service_tickets), reversed=True)
    
    return mechanic_schema.jsonify(mechanics)

@mechanics_bp.route("/search", methods=["GET"])
def search_mechanic():
    name = request.args.get("name")
    
    query = select(Mechanic).where(Mechanic.name.like(f'%{name}%'))
    mechanics = db.session.execute(query).scalars().all()
    
    return mechanics_schema.jsonify(mechanics)