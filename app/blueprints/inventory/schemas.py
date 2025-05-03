from app.models import Inventory
from app.extension import ma

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        
inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)