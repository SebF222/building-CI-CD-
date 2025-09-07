from app.extensions import ma
from app.models import Parts

class PartsSchema(ma.SQLAlchemyAutoSchema):
    desc_id = ma.Integer(required=True)  
    
    class Meta:
        model = Parts


parts_schema = PartsSchema()
all_parts_schema = PartsSchema(many=True)