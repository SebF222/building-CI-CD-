from app.extensions import ma
from app.models import Customers


class Customerschema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customers

customer_schema = Customerschema()
customers_schema = Customerschema(many=True)