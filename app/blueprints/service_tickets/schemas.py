from app.extensions import ma 
from app.models import Service_tickets


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_tickets
        include_fk = True

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)

