from flask import Flask, Response
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from utils.db import db
import os
import json

#Load environment variables from .env file
load_dotenv()

#Create Flask object
app = Flask(__name__)

#Define app parameters
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')

#Connect db object so app can access to database
db.init_app(app)

with app.app_context():
    #Get object for jwt
    jwt = JWTManager(app)

    #Include routes for users and tasks
    from routes.users_route import users_bp
    from routes.tasks_route import tasks_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(tasks_bp)

    #Default response for unauthorized requests
    @jwt.unauthorized_loader
    def message_unauthorized_access(error):
        return Response(json.dumps({'message': 'You need to be logged in to access this route'}), status=401, mimetype='application/json')