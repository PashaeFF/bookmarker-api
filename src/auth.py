from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from http import HTTPStatus
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, create_refresh_token
from flasgger import swag_from
from src.database import User, db

auth = Blueprint("auth",__name__,url_prefix="/api/v1/auth")

@auth.post('/register')
@swag_from('./docs/auth/register.yaml')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({'error': "Parol qisadir... Minimal 6 simvol olmalidir..."}), HTTPStatus.BAD_REQUEST 
    
    if len(username) < 3:
        return jsonify({'error': "Istifadechi adi minimum 3 simvol olmalidir..."}), HTTPStatus.BAD_REQUEST 
    
    if not username.isalnum() or " " in username:
        return jsonify({'error': "Istifadechi adi alfanumerik olmali ve boshluq olmamalidir..."}), HTTPStatus.BAD_REQUEST 
    
    if not validators.email(email):
        return jsonify({'error': "Email etibarli deyil..."}), HTTPStatus.BAD_REQUEST 
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email movcuddur..."}), HTTPStatus.CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': f"{username} adli istifadechi movcuddur..."}), HTTPStatus.CONFLICT
    
    pwd_hash = generate_password_hash(password)
    user = User(username = username, password = pwd_hash, email = email)
    # sebuhi_user = User(username = "username", password = "pwd_hash", email = "email")

    db.session.add(user)
    # db.session.add(sebuhi_user)

    db.session.commit()

    return jsonify({
        'message':"Istifadechi qeyd oldu",
        'user': {
            'username' : username, "email": email
        }
    }), HTTPStatus.CREATED


@auth.post('/login')
@swag_from('./docs/auth/login.yaml')
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')


    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity = user.id)
            access = create_access_token(identity = user.id)

            return jsonify({

                'user':{
                    'refresh':refresh,
                    'access':access,
                    'username':user.username,
                    'email':user.email
                }
            }), HTTPStatus.OK

    return jsonify({'error':'sehv bilgiler'}), HTTPStatus.UNAUTHORIZED


@auth.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    return({
        'username':user.username,
        'email':user.email
    }), HTTPStatus.OK

@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access':access
    }), HTTPStatus.OK
