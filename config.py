from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
# from .main import *
from api import api_bp

# initialize app
app = Flask(__name__)

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/journey' 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:8889/journey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_HASH']='bcrypt'

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)


# Session(app)
app.register_blueprint(api_bp)


# with app.app_context():
#     db.create_all()
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True)
