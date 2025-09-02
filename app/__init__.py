from flask import Flask
from .models import db
from app.extensions import ma , limiter, cache
from .blueprints.mechanics import mechanics_bp
from .blueprints.customers import customers_bp
from .blueprints.service_tickets import service_tickets_bp
from flask_swagger_ui import get_swaggerui_blueprint



SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': 'Mechanic Management API'} )


def create_app(config_name):
    app = Flask(__name__) #creating base app 
    app.config.from_object(f'config.{config_name}')

    
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)
    # app.regiester_blueprint(service_tickets_bp, url_prefix='/service_tickets') # make a new blueprint 

    return app 

