from app.extensions import ma
from app.models import Inventory

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True
        sqla_session = ma.auto_field

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)