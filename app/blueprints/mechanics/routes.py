from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema, login_schema
from flask import request, jsonify, session 
from app.blueprints.mechanics import mechanics_bp
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Mechanics, db
from . import mechanics_bp
from app.extensions import limiter
from app.utils.util import encode_token, token_required 


@mechanics_bp.route("/login", methods=["POST"])
def login():

    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Mechanics).where(Mechanics.email == email)
    mechanic = db.session.execute(query).scalars().first()

    if mechanic and mechanic.password == password:
        token = encode_token(mechanic.id)

        response = {
            "status": "success",
            "message": "successfully logged in.",
            "token": token
        }

        return jsonify(response), 200 
    else:
        return jsonify({"message": "Invalid email or password!"})
        
@mechanics_bp.route("", methods=['POST'])
@limiter.limit("10 per day")
def create_member():
    try:
        Mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanics).where(Mechanics.email == Mechanic_data['email'])
    new_mechanic =  Mechanics(address=Mechanic_data['address'], email=Mechanic_data['email'], first_name=Mechanic_data['first_name'], last_name=Mechanic_data['last_name'], DOB=Mechanic_data['DOB'], password=Mechanic_data['password'] )
    existing_Mechanic = db.session.execute(query).scalars().all()
    if existing_Mechanic:
        return jsonify({"error": "Email already associated with an account."}), 400
    
    new_mechanic = Mechanics(**Mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201 
    
@mechanics_bp.route("", methods=['GET'])
def get_mechanics():
    query = select(Mechanics)
    mechanics = db.session.execute(query).scalars().all()

    return mechanics_schema.jsonify(mechanics), 200 

@mechanics_bp.route("<int:mechanic_id>", methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)

    if mechanic:
        return mechanic_schema.jsonify(mechanic)
    return jsonify({"error": "mechanic not found."}), 400 


@mechanics_bp.route("/", methods=['PUT'])
@token_required
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not mechanic:
        return jsonify({"error": "mechanic not found."}), 400
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e: 
        return jsonify(e.messages), 400

    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200 

@mechanics_bp.route("/", methods=['DELETE'])
@token_required
def delete_mechanic(mechanic_id):
    # mechanic = db.session.get(Mechanics, mechanic_id)

    query = select(Mechanics).where(Mechanics.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()

  
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f'mechanic id {mechanic_id}, successfully deleted.'}), 200










