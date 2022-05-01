from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'f4b1fdd2c71bc06cf91664542a30bb9d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test123@localhost/kuba'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from dietAnalysys import routes
