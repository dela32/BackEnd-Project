from flask import Flask
from app.models import db
from app.extension import ma, limiter, cache
from app.blueprints.customers import customers_bp
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.inventory import inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

get_swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Your API's Name"
    }
)

def create_app(config_name):
    
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    # Add extensions to app
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    # registering blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(get_swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    
    
    
    
    return app