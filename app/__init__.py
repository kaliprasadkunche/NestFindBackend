#backend/app/__init__.py

from flask import Flask
from .extensions import db, jwt, socketio
from .routes import auth, listings, reviews, chat
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    
    app.config.from_object('app.config.Config')

    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app) 
    
    from flask_migrate import Migrate
    Migrate(app, db)

    app.register_blueprint(auth.bp)
    app.register_blueprint(listings.bp)
    app.register_blueprint(reviews.bp)
    app.register_blueprint(chat.bp)
    
    # Configure CORS to allow requests from the frontend
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    return app
