from flask import Blueprint

inventory_bp = Blueprint('inventory', __name__)


from .routes import inventory_bp