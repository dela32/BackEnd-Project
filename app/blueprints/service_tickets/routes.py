from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.service_tickets.schemas import service_ticket_schema, service_tickets_schema, EditServiceTicketSchema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import ServiceTicket, db, Mechanic, Inventory
from sqlalchemy import select, delete
from app.extension import cache
from app.utils.utils import encode_token, token_required


@service_tickets_bp.route("/", methods=["POST"])
def create_service_ticket():
    try:
       service_ticket_data = service_ticket_schema.load(request.json)
       print(service_ticket_data)
        
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service_ticket = ServiceTicket(VIN=service_ticket_data['VIN'], service_date=service_ticket_data['service_date'], service_desc = service_ticket_data['service_desc'], customer_id = service_ticket_data['customer_id'])
    
    for mechanic_id in service_ticket_data["mechanic_ids"]:
        query = select(Mechanic).where(Mechanic.id==mechanic_id)
        mechanic = db.session.execute(query).scalar()
        if mechanic:
            new_service_ticket.mechanics.append(mechanic)
        else:
            return jsonify({"message": "invalid mechanic id"}), 400
    
    db.session.add(new_service_ticket)
    db.session.commit()
    
    return service_ticket_schema.jsonify(new_service_ticket), 201

@service_tickets_bp.route("/", methods=['GET'])
@cache.cached(timeout=60)
# important to use cache here incase there are multiple request to view a service ticket
def get_service_tickets():
    query = select(ServiceTicket)
    result = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(result), 200

@service_tickets_bp.route("/my-tickets", methods=["GET"])
@token_required
def get_my_tickets(customer_id):
    query = select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200


@service_tickets_bp.route("/<int:service_ticket_id>", methods=['DELETE'])
def delete_service_ticket(service_ticket_id):
    query = select(ServiceTicket).where(ServiceTicket.id == service_ticket_id)
    service_ticket = db.session.execute(query).scalars().first()

    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": f"succesfully deleted service ticket {service_ticket_id}"})

@service_tickets_bp.route("/<int:service_ticket_id>", methods=['PUT']) #updating method
def edit_service_ticket(service_ticket_id):
    try: 
        edit_schema = EditServiceTicketSchema()
        service_ticket_edits = edit_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
        
    query = select(ServiceTicket).where(ServiceTicket.id == service_ticket_id)
    service_ticket = db.session.execute(query).scalars().first()
    
    for mechanic_id in service_ticket_edits['add_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()
    
        if mechanic and mechanic not in service_ticket.mechanics:
            service_ticket.mechanics.append(mechanic)


    for mechanic_id in service_ticket_edits['remove_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()
        
        if mechanic and mechanic in service_ticket.mechanics:
            service_ticket.mechanics.remove(mechanic)
            
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket)


@service_tickets_bp.route("/<int:ticket_id>/add-inventory/<int:inventory_id>", methods=["POST"])
def add_inventory_to_ticket(ticket_id, inventory_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    inventory = db.session.get(Inventory, inventory_id)

    if not ticket:
        return jsonify({"message": f"Service ticket {ticket_id} not found"}), 404
    if not inventory:
        return jsonify({"message": f"Part {inventory_id} not found in inventory"}), 404

    if inventory in ticket.inventory_items:
        return jsonify({"message": "Part already added to this ticket"}), 400

    ticket.inventory_items.append(inventory)
    db.session.commit()

    return jsonify({"message": f"Part '{inventory.name}' added to service ticket {ticket_id}"}), 200
