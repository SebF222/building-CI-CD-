from app.blueprints.customers.schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customers, db
from . import customers_bp
from app.extensions import limiter



@customers_bp.route("", methods=['POST'])
@limiter.limit("1000 per day")
def create_member():
    try:
        Customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customers).where(Customers.email == Customer_data['email'])
    existing_Customer = db.session.execute(query).scalars().all()
    if existing_Customer:
        return jsonify({"error": "Email already associated with an account."}), 400
    
    new_customer = Customers(**Customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

@customers_bp.route("", methods=['GET'])
def get_customers():
    query = select(Customers)
    customers = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(customers), 200

@customers_bp.route("<int:customer_id>", methods=['GET'])
@limiter.limit("25 per hour")
def get_customer(customer_id):
    customer = db.session.get(Customers, customer_id)

    if customer:
        return customer_schema.jsonify(customer)
    return jsonify({"error": "Customer not found."}), 400

@customers_bp.route("<int:customer_id>", methods=["PUT"])
@limiter.limit("50 per hour")
def update_customer(customer_id):
    customer = db.session.get(Customers, customer_id)

    if not customer:
        return jsonify({"error": "customer not found."}), 400
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)
    
    db.session.commit()
    return customer_schema.jsonify(customer), 200

@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
@limiter.limit("15 per hour")
def delete_customer(customer_id):
    customer = db.session.get(Customers, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "customer deleted successfully."}), 200 





