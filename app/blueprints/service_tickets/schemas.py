from app.models import Service_tickets
from marshmallow import fields
from app.extensions import ma 



class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanic_ids = fields.Method("get_mechanic_ids")

    class Meta:
        model = Service_tickets
        include_fk = True
        fields = ("id", "customers_id", "description", "price", "vin", "date")

    def get_mechanic_ids(self, obj):
        # Assumes obj.mechanics is a list of Mechanic objects with an id attribute
        return [mech.id for mech in getattr(obj, 'mechanics', [])]


class EditServiceTicketSchema(ma.Schema): 
    add_service_ticket_ids = fields.List(fields.Int(), required=True)
    remove_service_ticket_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_service_ticket_ids", "remove_service_ticket_ids")

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
return_service_ticket_schema = ServiceTicketSchema(exclude=['customers_id'])
edit_service_ticket_schema = EditServiceTicketSchema()




