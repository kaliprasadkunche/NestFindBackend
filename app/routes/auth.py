#backend/app/routes/auth.py

from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        user_type=data['user_type']
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity={'username': user.username, 'user_type': user.user_type, 'user_id': user.user_id, 'user_email': user.email})
        return jsonify(access_token=access_token, username=user.username, user_type=user.user_type, user_id=user.user_id, user_email=user.email), 200
    return jsonify({"message": "Invalid credentials"}), 401


@bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    identity = get_jwt_identity()
    user = User.query.get(identity['user_id'])
    data = request.get_json()
    
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    
    db.session.commit()
    return jsonify({
        "id": user.user_id,
        "username": user.username,
        "user_type": user.user_type,
        "user_email": user.email
    }), 200