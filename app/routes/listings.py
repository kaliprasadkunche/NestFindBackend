#backend/app/routes/listings.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Listing, User

bp = Blueprint('listings', __name__, url_prefix='/listings')

@bp.route('/', methods=['POST'], endpoint='create_listing')
@jwt_required()
def create_listing():
    current_user = get_jwt_identity()
    user_id = current_user['user_id']
    if current_user['user_type'] != 'Owner':
        return jsonify({"message": "Only Owners can create listings"}), 403
    
    house_name = request.form.get('house_name')
    owner_name = request.form.get('owner_name')
    contact_info = request.form.get('contact_info')
    house_type = request.form.get('house_type')
    room_type = request.form.get('room_type')
    city = request.form.get('city')
    location = request.form.get('location')
    area = request.form.get('area')
    street = request.form.get('street')
    price = request.form.get('price')
    google_map_location = request.form.get('google_map_location')
    images = [request.form.get(f'image{i+1}') for i in range(5)]

    new_listing = Listing(
        house_name=house_name, owner_name=owner_name, contact_info=contact_info,
        house_type=house_type, room_type=room_type, city=city, location=location, area=area, street=street, price=price,
        google_map_location=google_map_location, image1=images[0], image2=images[1], image3=images[2], image4=images[3], image5=images[4],
        user_id=user_id
    )
    db.session.add(new_listing)
    db.session.commit()
    return jsonify({"message": "Listing created successfully"}), 201

@bp.route('/<int:listing_id>', methods=['PUT'], endpoint='update_listing')
@jwt_required()
def update_listing(listing_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    if user.user_type != 'Owner':
        return jsonify({"message": "Only Owners can update listings"}), 403

    listing = Listing.query.get_or_404(listing_id)
    if listing.user_id != user.user_id:
        return jsonify({"message": "You can only update your own listings"}), 403

    house_name = request.form.get('house_name')
    owner_name = request.form.get('owner_name')
    contact_info = request.form.get('contact_info')
    house_type = request.form.get('house_type')
    room_type = request.form.get('room_type')
    city = request.form.get('city')
    location = request.form.get('location')
    area = request.form.get('area')
    street = request.form.get('street')
    price = request.form.get('price')
    google_map_location = request.form.get('google_map_location')
    images = [request.form.get(f'image{i+1}') for i in range(5)]

    listing.house_name = house_name
    listing.owner_name = owner_name
    listing.contact_info = contact_info
    listing.house_type = house_type
    listing.room_type = room_type
    listing.city = city
    listing.location = location
    listing.area = area
    listing.street = street
    listing.price = price
    listing.google_map_location = google_map_location
    listing.image1 = images[0]
    listing.image2 = images[1]
    listing.image3 = images[2]
    listing.image4 = images[3]
    listing.image5 = images[4]
    
    db.session.commit()
    return jsonify({"message": "Listing updated successfully"}), 200

@bp.route('/', methods=['GET'])
def get_listings():
    listings = Listing.query.all()
    return jsonify([{
        'id': listing.listing_id,
        'house_name': listing.house_name,
        'owner_name': listing.owner_name,
        'contact_info': listing.contact_info,
        'house_type': listing.house_type,
        'room_type': listing.room_type,
        'city': listing.city,
        'location': listing.location,
        'area': listing.area,
        'street': listing.street,
        'price': listing.price,
        'google_map_location': listing.google_map_location,
        'image1': listing.image1,
        'image2': listing.image2,
        'image3': listing.image3,
        'image4': listing.image4,
        'image5': listing.image5,
        'user_id': listing.user_id
    } for listing in listings]), 200

@bp.route('/<int:listing_id>', methods=['DELETE'])
@jwt_required()
def delete_listing(listing_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    if user.user_type != 'Owner':
        return jsonify({"message": "Only Owners can delete listings"}), 403

    listing = Listing.query.get_or_404(listing_id)
    if listing.user_id != user.user_id:
        return jsonify({"message": "You can only delete your own listings"}), 403

    db.session.delete(listing)
    db.session.commit()
    return jsonify({"message": "Listing deleted successfully"}), 200
