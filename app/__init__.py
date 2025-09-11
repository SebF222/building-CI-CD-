from flask import Flask
from .models import db
from app.extensions import ma , limiter, cache
from .blueprints.mechanics import mechanics_bp
from .blueprints.customers import customers_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.parts import parts_bp
from .blueprints.inventory import inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint #need this to create a blueprint toplug into the app were making 



SWAGGER_URL = '/api/docs' #url for exposing my swagger ui
API_URL = '/static/swagger.yaml' #What connects us to the host 



# creating swagger blueprint
swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': 'Mechanic Management API'} ) 


def create_app(config_name):  #Application Factory
    app = Flask(__name__) #creating base app 
    app.config.from_object(f'config.{config_name}')

    #initialize the extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    
    
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')
    app.register_blueprint(parts_bp, url_prefix='/parts')
    app.register_blueprint(inventory_bp, url_prefix='/inventory') 
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL) #Regestering Swagger blueprint to make it accessible on the app

    return app 

