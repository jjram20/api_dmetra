from flask import Blueprint, request, Response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request
from utils.db import db
from models.user import User
from datetime import timedelta
import json
import re

users_bp = Blueprint('users', __name__)

#Route to register new users
@users_bp.post("/register")
def register():
    try:
        req = request.get_json(force=True)
        email = req.get('email')
        password = req.get('password')
        #Confirm data required is included
        if email and password:
            #Check email conditions
            email_db = User.query.filter_by(email=email).first()
            if not email_db:
                #Examine email format is correct
                re_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if re.match(re_pattern, email) is None:
                    return Response(json.dumps({'message': 'Incorrect email format'}), mimetype='application/json')
                else:
                    #Hashing password
                    hash_password = generate_password_hash(password)
                    #Save new user
                    new_user = User(email, hash_password)
                    db.session.add(new_user)
                    db.session.flush()
                    db.session.commit()
                    return Response(json.dumps({'message': 'Email registered'}), status=200, mimetype='application/json')
            else:
                return Response(json.dumps({'message': 'Email previously registered'}), status=409, mimetype='application/json')
        else:
            return Response(json.dumps({'message': 'There is no enough data to process request'}), status=400, mimetype='application/json')
    #In case any unexpected error
    except Exception as error:
        print(error)
        return Response(json.dumps({'message': 'Error processing request'}), status=500, mimetype='application/json')

#Route for logging
@users_bp.post("/login")
def login():
    try:
        #Check if previous sessions exist
        verify_jwt_in_request(optional=True)
        current_user = get_jwt_identity()
        if current_user:
            return Response(json.dumps({'message': 'User already logged in'}), status=200, mimetype='application/json')
        else:
            #Get user information
            req = request.get_json(force=True)
            email = req.get('email')
            user_db = User.query.filter_by(email=email).first()
            password = req.get('password')
            #Verify password
            if user_db and check_password_hash(user_db.password, password):
                access_token = create_access_token(identity=user_db.id, expires_delta=timedelta(hours=12))
                return Response(json.dumps({'message': 'Sucessful login', 'access_token': access_token}), status=200, mimetype='application/json')
            else:
                return Response(json.dumps({'message': 'Login failed, incorrect email and/or password'}), status=400)
    #In case any unexpected error
    except Exception as error:
        print(error)
        return Response(json.dumps({'message': 'Error processing request'}), status=500)