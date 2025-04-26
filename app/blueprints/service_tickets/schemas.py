from app.models import ServiceTicket
from app.extension import ma
from marshmallow import fields

class Service_TicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested("MechaicsSchema", many=True)
    customer = fields.Nested("CustomerSchema")
    class Meta:
        model = ServiceTicket
        fields = ("id", "VIN", "service_date", "service_desc", "customer_id", "customer", "mechanincs", "mechanic_ids",)
        
service_ticket_schema = Service_TicketSchema()
service_tickets_schema = Service_TicketSchema(many=True)