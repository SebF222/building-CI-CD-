# Parts and Inventory CRUD routes using user's code style
from flask import request, jsonify
from app.models import db, Parts, Inventory, Service_tickets
from app.blueprints.parts.schemas import PartsSchema,  parts_schema ,all_parts_schema 
from marshmallow import ValidationError
from sqlalchemy import select
from . import parts_bp  # Import the blueprint from __init__.py
from app.utils.util import encode_token, token_required


# Create Inventory Item

@parts_bp.route("", methods=['GET'])
def get_parts():
    query = select(Parts)
    parts = db.session.execute(query).scalars().all()

    return all_parts_schema.jsonify(parts), 200

@parts_bp.route("", methods=['POST'])
def create_part():
    try:
        part_data = parts_schema.load(request.json)
    except ValidationError as e: 
        return jsonify(e.messages), 400
    
    
    inventory = db.session.get(Inventory, part_data['desc_id'])
    if not inventory:
        return jsonify({"error": "Inventory item not found."}), 400 
    
    if part_data.get('ticket_id'): 
        ticket = db.session.get(Service_tickets, part_data['ticket_id'])
        if not ticket:
            return jsonify({"error": "Service ticket not found."}), 400

    new_part = Parts(**part_data)
    db.session.add(new_part)
    db.session.commit()
    return parts_schema.jsonify(new_part), 201

@parts_bp.route("/<int:part_id>", methods=['GET'])
def get_part(part_id):
    part = db.session.get(Parts, part_id)

    if part:
        return parts_schema.jsonify(part)
    return jsonify({"error": "Part not found."}), 400

@parts_bp.route("/<int:part_id>", methods=['PUT'])
def update_part(part_id):
    part = db.session.get(Parts, part_id)

    if not part:
        return jsonify({"error": "Part not found."}), 400
    
    try:
        part_data = parts_schema.load(request.json, partial=True)
    except ValidationError as e: 
        return jsonify(e.messages), 400

    if 'desc_id' in part_data:  # ✅ Dictionary check
        inventory = db.session.get(Inventory, part_data['desc_id'])  # ✅ Dictionary access
        if not inventory:
            return jsonify({"error": "Inventory item not found."}), 400
    
    if 'ticket_id' in part_data and part_data['ticket_id']:  # ✅ Dictionary check
        ticket = db.session.get(Service_tickets, part_data['ticket_id'])  # ✅ Dictionary access
        if not ticket:
            return jsonify({"error": "Service ticket not found."}), 400

    for key, value in part_data.items():  # ✅ Dictionary iteration
        setattr(part, key, value)

    db.session.commit()
    return parts_schema.jsonify(part), 200

@parts_bp.route("/<int:part_id>", methods=['DELETE'])
def delete_part(part_id):
    query = select(Parts).where(Parts.id == part_id)
    part = db.session.execute(query).scalars().first()

    if not part:
        return jsonify({"error": "Id not found"}), 404

    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f'Part id {part_id}, successfully deleted.'}), 200

@parts_bp.route("/by-ticket/<int:ticket_id>", methods=['GET'])
def get_parts_by_ticket(ticket_id):
    from app.models import Service_tickets
    
    ticket = db.session.get(Service_tickets, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404
        
    query = select(Parts).where(Parts.ticket_id == ticket_id)
    parts = db.session.execute(query).scalars().all()
    
    return all_parts_schema.jsonify(parts), 200

@parts_bp.route("/by-inventory/<int:inventory_id>", methods=['GET'])
def get_parts_by_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)
    if not inventory:
        return jsonify({"error": "Inventory not found"}), 404
        
    query = select(Parts).where(Parts.desc_id == inventory_id)
    parts = db.session.execute(query).scalars().all()
    
    return all_parts_schema.jsonify(parts), 200

@parts_bp.route("/unassigned", methods=['GET'])
def get_unassigned_parts():
    query = select(Parts).where(Parts.ticket_id.is_(None))
    parts = db.session.execute(query).scalars().all()
    
    return all_parts_schema.jsonify(parts), 200