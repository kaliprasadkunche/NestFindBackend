# backend/app/routes/chat.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Chat, Message, User, Listing

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/start', methods=['POST'])
@jwt_required()
def start_chat():
    current_user = get_jwt_identity()
    tenant_id = current_user['user_id']
    listing_id = request.json.get('listing_id')

    listing = Listing.query.get_or_404(listing_id)
    owner_id = listing.user_id

    existing_chat = Chat.query.filter_by(tenant_id=tenant_id, owner_id=owner_id, listing_id=listing_id).first()
    if existing_chat:
        return jsonify({"chat_id": existing_chat.chat_id}), 200

    new_chat = Chat(tenant_id=tenant_id, owner_id=owner_id, listing_id=listing_id)
    db.session.add(new_chat)
    db.session.commit()

    return jsonify({"chat_id": new_chat.chat_id}), 201

@bp.route('/<int:chat_id>/messages', methods=['POST'])
@jwt_required()
def send_message(chat_id):
    current_user = get_jwt_identity()
    sender_id = current_user['user_id']
    content = request.json.get('content')

    new_message = Message(chat_id=chat_id, sender_id=sender_id, content=content)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({"message": "Message sent"}), 201

@bp.route('/<int:chat_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(chat_id):
    messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.timestamp).all()
    return jsonify([{
        'message_id': message.message_id,
        'chat_id': message.chat_id,
        'sender_id': message.sender_id,
        'content': message.content,
        'timestamp': message.timestamp
    } for message in messages]), 200

@bp.route('/user-chats', methods=['GET'])
@jwt_required()
def get_user_chats():
    current_user = get_jwt_identity()
    user_id = current_user['user_id']

    chats_as_tenant = Chat.query.filter_by(tenant_id=user_id).all()
    chats_as_owner = Chat.query.filter_by(owner_id=user_id).all()

    chats = chats_as_tenant + chats_as_owner

    return jsonify([{
        'chat_id': chat.chat_id,
        'tenant_id': chat.tenant_id,
        'owner_id': chat.owner_id,
        'listing_id': chat.listing_id,
        'created_at': chat.created_at
    } for chat in chats]), 200
