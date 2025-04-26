from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.service_tickets.schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from . import service_tickets_bp
from marshmallow import ValidationError
from app.models import ServiceTicket, db, Mechanic
from sqlalchemy import select, delete

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
def get_service_tickets():
    query = select(ServiceTicket)
    result = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(result), 200


@service_tickets_bp.route("/<int:service_ticket_id>", methods=['DELETE'])
def delete_service_ticket(service_ticket_id):
    query = select(ServiceTicket).where(ServiceTicket.id == service_ticket_id)
    service_ticket = db.session.execute(query).scalars().first()

    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": f"succesfully deleted service ticket {service_ticket_id}"})