from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__, template_folder='templates')
app.config.from_object('config')
db = SQLAlchemy(app)
admin = Admin(app,template_mode='bootstrap4')
migrate = Migrate(app, db, render_as_batch=True)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import views, models, forms