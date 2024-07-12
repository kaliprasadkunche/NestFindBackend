#backend/run.py

from app import create_app
from flask_migrate import Migrate
from app.extensions import db, socketio
from flask_cors import CORS



app = create_app()
migrate = Migrate(app, db)
CORS(app, origins='http://localhost:3000')


if __name__ == "__main__":
    app.run(debug=True)


#venv\Scripts\activate
#python run.py