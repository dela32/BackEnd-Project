from app.models import Mechanic
from app.extension import ma

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)