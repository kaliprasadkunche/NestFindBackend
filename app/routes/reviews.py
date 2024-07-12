from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Review, User

bp = Blueprint('reviews', __name__, url_prefix='/reviews')


@bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    data = request.get_json()
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    
    if user.user_type != 'Tenant':
        return jsonify({"message": "Only Tenants can create reviews"}), 403

    new_review = Review(
        rating=data['rating'], comment=data['comment'],
        listing_id=data['listing_id'], user_id=user.id
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({"message": "Review created successfully"}), 201


@bp.route('/<int:listing_id>', methods=['GET'])
def get_reviews(listing_id):
    reviews = Review.query.filter_by(listing_id=listing_id).all()
    return jsonify([{
        'id': review.review_id,
        'rating': review.rating,
        'comment': review.comment,
        'listing_id': review.listing_id,
        'user_id': review.user_id
    } for review in reviews]), 200
