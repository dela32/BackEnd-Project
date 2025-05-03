from app.models import ServiceTicket
from app.extension import ma
from marshmallow import fields

class Service_TicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested("MechaicsSchema", many=True)
    customer = fields.Nested("CustomerSchema")
    class Meta:
        model = ServiceTicket
        fields = ("id", "VIN", "service_date", "service_desc", "customer_id", "customer", "mechanincs", "mechanic_ids",)
        
class EditServiceTicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required = True)
    remove_mechanic_ids = fields.List(fields.Int(), required = True)
    
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")

service_ticket_schema = Service_TicketSchema()
service_tickets_schema = Service_TicketSchema(many=True)
return_service_tickets_schema = Service_TicketSchema(exclude=['customer_id'])
edit_service_tickets_schema = EditServiceTicketSchema()