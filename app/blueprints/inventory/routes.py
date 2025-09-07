from flask import Blueprint, request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from app import db
from app.models import Inventory
from app.blueprints.inventory.schemas import inventory_schema, inventories_schema
from . import inventory_bp

inventory_bp = Blueprint('inventory', __name__)
@inventory_bp.route("", methods=['GET'])
def get_inventories():
    query = select(Inventory)
    inventories = db.session.execute(query).scalars().all()

    return inventories_schema.jsonify(inventories), 200

@inventory_bp.route("", methods=['POST'])
def create_inventory():
    try:
        Inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Inventory).where(Inventory.name == Inventory_data.name) 
    existing_inventory = db.session.execute(query).scalars().first()  
    if existing_inventory:
        return jsonify({"error": "Inventory item with this name already exists."}), 400
   
    db.session.add(Inventory_data)  
    db.session.commit()
    return inventory_schema.jsonify(Inventory_data), 201  

@inventory_bp.route("/<int:inventory_id>", methods=['GET'])
def get_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)

    if inventory:
        return inventory_schema.jsonify(inventory)
    return jsonify({"error": "Inventory not found."}), 400

@inventory_bp.route("/<int:inventory_id>", methods=['PUT'])
def update_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)

    if not inventory:
        return jsonify({"error": "Inventory not found."}), 400
    
    try:
        inventory_data = inventory_schema.load(request.json, partial=True)
    except ValidationError as e: 
        return jsonify(e.messages), 400

    # Update the inventory with new data
    for key in inventory_data.__dict__:
        if not key.startswith('_'):
            setattr(inventory, key, getattr(inventory_data, key))

    db.session.commit()
    return inventory_schema.jsonify(inventory), 200

@inventory_bp.route("/<int:inventory_id>", methods=['DELETE'])
def delete_inventory(inventory_id):
    query = select(Inventory).where(Inventory.id == inventory_id)
    inventory = db.session.execute(query).scalars().first()

    db.session.delete(inventory)
    db.session.commit()
    return jsonify({"message": f'Inventory id {inventory_id}, successfully deleted.'}), 200

@inventory_bp.route("/<int:inventory_id>/parts", methods=['GET'])
def get_inventory_parts(inventory_id):
    from app.models import Parts
    from app.blueprints.parts.schemas import all_parts_schema
    
    inventory = db.session.get(Inventory, inventory_id)
    if not inventory:
        return jsonify({"error": "Inventory not found"}), 404
        
    query = select(Parts).where(Parts.desc_id == inventory_id)
    parts = db.session.execute(query).scalars().all()
    
    return all_parts_schema.jsonify(parts), 200