from app.blueprints.inventory import inventory_bp
from app.blueprints.inventory.schemas import inventory_schema, inventories_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Inventory, db
from sqlalchemy import select
from app.extension import cache

@inventory_bp.route("/", methods=["POST"])
def create_inventory():
    try:
        inventory_data = inventory_schema.load(request.json)
        print(inventory_data)
        
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_inventory = Inventory(name=inventory_data['name'], price=inventory_data['price'])
    db.session.add(new_inventory)
    db.session.commit()
    
    return inventory_schema.jsonify(new_inventory), 200


@inventory_bp.route("/", methods=['GET'])
@cache.cached(timeout=60)
def get_inventory():
    query = select(Inventory)
    result = db.session.execute(query).scalars().all()
    return inventories_schema.jsonify(result), 200


@inventory_bp.route("/search-inventory", methods=["GET"])
def search_inventory():
    name = request.args.get("name")
    
    query = select(Inventory).where(Inventory.name.like(f'%{name}%'))
    inventories = db.session.execute(query).scalars().all()
    
    return inventories_schema.jsonify(inventories)


@inventory_bp.route("<int:inventory_id>", methods=["PUT"])
def update_inventory(inventory_id):
    query = select(Inventory).where(Inventory.id == inventory_id)
    inventory = db.session.execute(query).scalars().first()
    print(inventory)
    
    if inventory == None:
        return jsonify({"message": "invalid inventory id"})
    
    try:
        inventory_data = inventory_schema.load(request.json)
        print(inventory_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in inventory_data.items():
        setattr(inventory, field, value)
        
    db.session.commit()
    return inventory_schema.jsonify(inventory), 200


@inventory_bp.route("/<int:inventory_id>", methods=["DELETE"])
def delete_inventory(inventory_id):
    query = select(Inventory).where(Inventory.id == inventory_id)
    inventory = db.session.execute(query).scalars().first()
    
    db.session.delete(inventory)
    db.session.commit()
    return jsonify({"message": f"successfully deleted inventory {inventory_id}"})
