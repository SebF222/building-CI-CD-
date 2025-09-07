from . import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema, edit_service_ticket_schema , return_service_ticket_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Service_tickets, Mechanics, db, Parts, Inventory, ticket_parts
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


@service_tickets_bp.route("/<int:ticket_id>", methods=['PUT'])
def edit_ticket(ticket_id):
    try:
        ticket_edit = edit_service_ticket_schema(request.json)
    except ValidationError as e:
        return jsonify(e.message), 400 
    
    query = select(Service_tickets).where(ticket.id == ticket_id)
    ticket = db.session.execute(query).scalars().first()

    for mechanic_id in ticket_edit['add_mechanic_ids']:
        query + select(mechanic).where(mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic not in ticket:
            ticket.mechanics.append(mechanic)

        
    for mechanic_id in ticket_edit['remove_mechanic_ids']:
        query + select(mechanic).where(mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic  in ticket:
            ticket.mechanics.remove(mechanic)

    db.session.commit()
    return return_service_ticket_schema.jsonify(ticket)




@service_tickets_bp.route("/<int:ticket_id>", methods=['DELETE'])
def delete_ticket(ticket_id):
    query = select(Service_tickets).where(Service_tickets.id == ticket_id)
    ticket = db.session.execute(query).scalars().first()

    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted service ticket {ticket_id}"}), 200



@service_tickets_bp.route("/<int:ticket_id>/add-part", methods=['POST'])
def add_part_to_ticket(ticket_id):
    ticket = db.session.get(Service_tickets, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    
    data = request.get_json()
    if not data or 'inventory_id' not in data:
        return jsonify({"error": "Inventory ID is required"}), 400
        
    inventory = db.session.get(Inventory, data['inventory_id'])
    if not inventory:
        return jsonify({"error": "Inventory item not found"}), 404
    
    # Create new part and associate it with the ticket
    new_part = Parts(desc_id=inventory.id)
    db.session.add(new_part)
    db.session.flush()  # Get the ID of the new part
    
    # Create the relationship with quantity
    ticket_part = ticket_parts(
        ticket_id=ticket.id,
        part_id=new_part.id,
        quantity=data.get('quantity', 1)  # Default to 1 if not specified
    )
    db.session.add(ticket_part)
    db.session.commit()
    
    return jsonify({
        "message": f"Part {inventory.name} added to ticket {ticket.id}",
        "part": {
            "id": new_part.id,
            "inventory_name": inventory.name,
            "price": inventory.price,
            "quantity": ticket_part.quantity
        }
    }), 201

@service_tickets_bp.route("", methods=['GET'])
@cache.cached(timeout=60)
def get_service_tickets():
    tickets = db.session.query(Service_tickets).all()
    return service_tickets_schema.jsonify(tickets), 200

