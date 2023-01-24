from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from api import api_bp
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
# from flask_session import Session

# initialize app
app = Flask(__name__)

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5433/journey' 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:8889/journey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_HASH']='bcrypt'
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Session(app)
app.register_blueprint(api_bp)


with app.app_context():
    db.create_all()

