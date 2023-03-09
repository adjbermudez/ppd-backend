import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from api.routes import api
from api.models import db
from flask_jwt_extended import JWTManager
from datetime import timedelta


app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
CORS(app)


# database configuration
db_url = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
    "postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('FLASK_APP_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=12)
jwt = JWTManager(app)

MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0,0,0,0', port=PORT, debug=True)
