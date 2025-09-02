from . import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Service_tickets, Mechanics, db
from app.blueprints.mechanics.schemas import mechanics_schema
from app.extensions import cache, limiter



@service_tickets_bp.route("", methods=['POST'])
def create_service_ticket():
    try:
        data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_ticket = Service_tickets(**data)
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201

@service_tickets_bp.route('/<int:ticket_id>/add-mechanic/<int:mechanic_id>', methods=['PUT'])
def add_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Service_tickets,ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)

    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()
        return jsonify({
            "message": f"Mechanic {mechanic.first_name} {mechanic.last_name} {mechanic.id} has been added to this ticket {ticket.id}.",
            "ticket": service_ticket_schema.dump(ticket),
            "mechanic": mechanics_schema.dump(ticket.mechanics)

        }) , 200 
    return jsonify({"error": f"Mechanic {mechanic.last_name} is already assigned to this ticket."}), 400

@service_tickets_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Service_tickets, ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)

    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()
        return jsonify({
            "message": f"Mechanic {mechanic.first_name} {mechanic.last_name} {mechanic.id} has been removed from this ticket {ticket.id}.",
            "ticket": service_ticket_schema.dump(ticket),
            "mechanic": mechanics_schema.dump(ticket.mechanic)
        })
    
    return jsonify("This mechanic is no longer assigned to this ticket."), 400

@service_tickets_bp.route("", methods=['GET'])
@cache.cached(timeout=60)
def get_service_tickets():
    tickets = db.session.query(Service_tickets).all()
    return service_tickets_schema.jsonify(tickets), 200

