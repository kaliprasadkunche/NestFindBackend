#backend/app/models/__init__.py

from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(500), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)  # provider or seeker

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Listing(db.Model):
    listing_id = db.Column(db.Integer, primary_key=True)
    house_name = db.Column(db.String(120), nullable=False)
    owner_name = db.Column(db.String(120), nullable=False)
    contact_info = db.Column(db.String(120), nullable=False)
    house_type = db.Column(db.String(120), nullable=False)
    room_type = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    area = db.Column(db.String(120), nullable=False)
    street = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    google_map_location = db.Column(db.String, nullable=False)
    image1 = db.Column(db.String, nullable=True)
    image2 = db.Column(db.String, nullable=True)
    image3 = db.Column(db.String, nullable=True)
    image4 = db.Column(db.String, nullable=True)
    image5 = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, nullable=False)  # No ForeignKey constraint

class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    listing_id = db.Column(db.Integer, nullable=False)  # No ForeignKey constraint
    user_id = db.Column(db.Integer, nullable=False)  # No ForeignKey constraint
    
class Chat(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.listing_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    tenant = db.relationship('User', foreign_keys=[tenant_id])
    owner = db.relationship('User', foreign_keys=[owner_id])
    listing = db.relationship('Listing', foreign_keys=[listing_id])

class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.chat_id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    chat = db.relationship('Chat', backref=db.backref('messages', lazy=True))
    sender = db.relationship('User')